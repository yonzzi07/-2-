from quiz import Quiz

def get_default_quizzes():
    return [
        Quiz("기준금리를 결정하는 한국의 기관은?", ["기획재정부", "한국은행", "금융감독원", "한국거래소"], 2),
        Quiz("물가가 계속 오르는 현상은?", ["디플레이션", "인플레이션", "스태그네이션", "리세션"], 2),
        Quiz("기준금리를 올리면 보통 어떻게 될까?", ["대출이 늘어난다", "물가가 급등한다", "예금 금리가 오른다", "환율이 무조건 오른다"], 3),
        Quiz("원/달러 환율이 오르면 유리한 쪽은?", ["수출 기업", "해외여행객", "수입 기업", "해외 유학생"], 1),
        Quiz("경기 침체 속에서 물가가 오르는 현상은?", ["인플레이션", "디플레이션", "스태그플레이션", "리플레이션"], 3)
    ]


class QuizGame:
    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None
    
    def show_menu(self):
        print("=" * 40)
        print("나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)
    
    def get_number(self, prompt, min_value, max_value):
        while True:
            text = input(prompt).strip()
            if text == "":
                print("입력이 비었습니다. 다시 입력하세요.")
                continue
            try:
                number = int(text)
            except ValueError:
                print(f"숫자를 입력하세요. ({min_value}-{max_value})")
                continue
            if not (min_value <= number <= max_value):
                print(f"{min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue
            return number

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"퀴즈를 시작합니다! (총 {total}문제)")
        print("-" * 40)

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = self.get_number("정답 입력: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("정답입니다!")
                correct += 1
            else:
                answer_text = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번 {answer_text}입니다.")
            
            print("-" * 40)
        
        score = round(correct / total * 100)
        print("=" * 40)
        print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)




    def run(self):
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 5)
            if choice == 1:
                self.play_quiz()
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break
            else:
                print("준비 중인 기능입니다.")

