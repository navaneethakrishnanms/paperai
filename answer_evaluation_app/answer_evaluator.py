from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from difflib import SequenceMatcher
import re

class AnswerEvaluator:
    def __init__(self, vector_db_manager):
        """Initialize answer evaluator with vector DB manager"""
        self.vector_db = vector_db_manager
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=5000,
            stop_words='english'
        )
    
    def evaluate_answers(self, student_answers):
        """
        Evaluate student answers against answer key
        Returns detailed evaluation results
        """
        try:
            # Get all questions and answers from vector DB
            questions = self.vector_db.get_all_questions()
            answer_key = self.vector_db.get_all_answers()
            
            if not questions:
                raise Exception("No question paper loaded. Please upload question paper first.")
            
            if not answer_key:
                raise Exception("No answer key loaded. Please upload answer key first.")
            
            # Create question and answer dictionaries for quick lookup
            questions_dict = {q['question_number']: q for q in questions}
            answers_dict = {a['question_number']: a for a in answer_key}
            
            # Evaluate each student answer
            question_wise_marks = []
            total_marks = 0
            obtained_marks = 0
            
            # Get all question numbers from questions_dict
            all_question_numbers = sorted(questions_dict.keys())
            
            for q_num in all_question_numbers:
                question = questions_dict.get(q_num)
                correct_answer = answers_dict.get(q_num)
                
                if not question:
                    continue
                
                max_marks = question['max_marks']
                total_marks += max_marks
                
                # Find student's answer for this question
                student_answer_obj = next((sa for sa in student_answers if sa['question_number'] == q_num), None)
                
                if not student_answer_obj:
                    # Student didn't answer this question
                    question_wise_marks.append({
                        'question_number': q_num,
                        'max_marks': max_marks,
                        'marks_obtained': 0,
                        'similarity_score': 0,
                        'feedback': 'Not answered'
                    })
                    continue
                
                student_answer = student_answer_obj['student_answer']
                
                if not correct_answer:
                    # No answer key for this question, give benefit of doubt
                    marks_awarded = max_marks * 0.7  # Award 70% if answer key missing
                    question_wise_marks.append({
                        'question_number': q_num,
                        'max_marks': max_marks,
                        'marks_obtained': round(marks_awarded, 2),
                        'similarity_score': 0.7,
                        'feedback': 'Answer key not available - partial marks awarded'
                    })
                    obtained_marks += marks_awarded
                    continue
                
                # Compare answers
                similarity_score = self._calculate_similarity(
                    student_answer,
                    correct_answer['answer_text']
                )
                
                # Calculate marks based on similarity
                marks_awarded = self._calculate_marks(similarity_score, max_marks)
                obtained_marks += marks_awarded
                
                # Generate feedback
                feedback = self._generate_feedback(similarity_score)
                
                question_wise_marks.append({
                    'question_number': q_num,
                    'max_marks': max_marks,
                    'marks_obtained': round(marks_awarded, 2),
                    'similarity_score': round(similarity_score, 3),
                    'feedback': feedback
                })
            
            # Calculate percentage
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            evaluation_result = {
                'total_marks': total_marks,
                'obtained_marks': round(obtained_marks, 2),
                'percentage': round(percentage, 2),
                'question_wise_marks': question_wise_marks
            }
            
            return evaluation_result
            
        except Exception as e:
            print(f"Error evaluating answers: {str(e)}")
            raise
    
    def _calculate_similarity(self, student_answer, correct_answer):
        """
        Calculate similarity between student answer and correct answer
        Uses multiple methods for robust comparison
        """
        try:
            # Clean and normalize answers
            student_clean = self._clean_text(student_answer)
            correct_clean = self._clean_text(correct_answer)
            
            if not student_clean or not correct_clean:
                return 0.0
            
            # Method 1: TF-IDF + Cosine Similarity
            try:
                tfidf_matrix = self.vectorizer.fit_transform([correct_clean, student_clean])
                cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            except:
                cosine_sim = 0.0
            
            # Method 2: Sequence Matcher (character-level similarity)
            sequence_sim = SequenceMatcher(None, correct_clean, student_clean).ratio()
            
            # Method 3: Word overlap similarity
            word_overlap_sim = self._word_overlap_similarity(student_clean, correct_clean)
            
            # Method 4: Keyword matching
            keyword_sim = self._keyword_similarity(student_clean, correct_clean)
            
            # Combine all similarities with weights
            combined_similarity = (
                cosine_sim * 0.35 +
                sequence_sim * 0.25 +
                word_overlap_sim * 0.25 +
                keyword_sim * 0.15
            )
            
            # Ensure similarity is between 0 and 1
            combined_similarity = max(0.0, min(1.0, combined_similarity))
            
            return combined_similarity
            
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        return text.strip()
    
    def _word_overlap_similarity(self, text1, text2):
        """Calculate word overlap similarity"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _keyword_similarity(self, student_text, correct_text):
        """Calculate similarity based on important keywords"""
        # Extract important words (longer than 4 characters)
        student_keywords = set([w for w in student_text.split() if len(w) > 4])
        correct_keywords = set([w for w in correct_text.split() if len(w) > 4])
        
        if not correct_keywords:
            return 0.0
        
        matched_keywords = student_keywords.intersection(correct_keywords)
        
        return len(matched_keywords) / len(correct_keywords)
    
    def _calculate_marks(self, similarity_score, max_marks):
        """
        Calculate marks based on similarity score
        Uses a grading curve
        """
        if similarity_score >= 0.90:
            return max_marks  # Full marks
        elif similarity_score >= 0.80:
            return max_marks * 0.95  # 95%
        elif similarity_score >= 0.70:
            return max_marks * 0.85  # 85%
        elif similarity_score >= 0.60:
            return max_marks * 0.75  # 75%
        elif similarity_score >= 0.50:
            return max_marks * 0.65  # 65%
        elif similarity_score >= 0.40:
            return max_marks * 0.55  # 55%
        elif similarity_score >= 0.30:
            return max_marks * 0.45  # 45%
        elif similarity_score >= 0.20:
            return max_marks * 0.30  # 30%
        elif similarity_score >= 0.10:
            return max_marks * 0.20  # 20%
        else:
            return max_marks * 0.10  # Minimum 10% for attempting
    
    def _generate_feedback(self, similarity_score):
        """Generate feedback based on similarity score"""
        if similarity_score >= 0.90:
            return "Excellent answer! Matches the key answer very closely."
        elif similarity_score >= 0.80:
            return "Very good answer! Most key points covered."
        elif similarity_score >= 0.70:
            return "Good answer. Covered major points."
        elif similarity_score >= 0.60:
            return "Satisfactory answer. Some important points covered."
        elif similarity_score >= 0.50:
            return "Average answer. Missing several key points."
        elif similarity_score >= 0.40:
            return "Below average. Many key points missing."
        elif similarity_score >= 0.30:
            return "Weak answer. Most key points not covered."
        elif similarity_score >= 0.20:
            return "Poor answer. Very few relevant points."
        else:
            return "Inadequate answer. Does not match expected content."
