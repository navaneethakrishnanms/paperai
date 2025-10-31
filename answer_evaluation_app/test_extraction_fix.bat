@echo off
echo ============================================
echo Testing Fixed Question/Answer Extraction
echo ============================================
echo.

python -c "from pdf_processor import PDFProcessor; p = PDFProcessor(); q = p.extract_questions_with_marks('uploads/question_paper_question.pdf'); a = p.extract_answers('uploads/answer_key_Ans.pdf'); print(f'\n✅ Questions extracted: {len(q)}'); print(f'✅ Answers extracted: {len(a)}')"

echo.
echo ============================================
echo Test Complete!
echo ============================================
pause
