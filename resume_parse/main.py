from parser import extract_text
from matcher import get_match_score_and_explanation
from excel_handler import append_to_excel

def main():
    print("Enter path to Job Description (pdf/docx):")
    jd_path = input().strip()
    jd_text = extract_text(jd_path)

    while True:
        print("Enter path to Resume (pdf/docx) or 'exit' to quit:")
        resume_path = input().strip()
        if resume_path.lower() == 'exit':
            break
        try:
            resume_text = extract_text(resume_path)
            score, explanation = get_match_score_and_explanation(resume_text, jd_text)
            if score is None:
                print("Could not parse score. Explanation:\n", explanation)
            else:
                print(f"Match Score: {score}\nExplanation:\n{explanation}")
                append_to_excel({
                    'Resume': resume_path,
                    'Score': score,
                    'Explanation': explanation
                })
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

