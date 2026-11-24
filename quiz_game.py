import json
from pathlib import Path

from quiz import Quiz

STATE_PATH = Path(__file__).parent / "state.json"


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
        self.reset_to_default()
        self.load_state()
    
    def reset_to_default(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    def is_valid_quiz_data(self, item):
        if not isinstance(item, dict):
            return False
        question = item.get("question")
        choices = item.get("choices")
        answer = item.get("answer")
        if not isinstance(question, str) or question.strip() == "":
            return False
        if not isinstance(choices, list) or len(choices) != 4:
            return False
        for choice in choices:
            if not isinstance(choice, str) or choice.strip() == "":
                return False
        if not isinstance(answer, int):
            return False
        return 1 <= answer <= 4


    def load_state(self):
        if not STATE_PATH.exists():
            print("저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = []
            for item in data["quizzes"]:
                if not self.is_valid_quiz_data(item):
                    raise ValueError("잘못된 퀴즈 데이터")
                quizzes.append(Quiz.from_dict(item))
            self.quizzes = quizzes
            self.best_score = data.get("best_score")
            self.best_correct = data.get("best_correct")
            self.best_total = data.get("best_total")
            if self.best_score is None:
                score_text = "최고 점수 없음"
            else:
                score_text = f"최고 점수 {self.best_score}점"
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, {score_text})")



        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.reset_to_default()
            self.save_state()
        except OSError:
            print("데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            self.reset_to_default()

    
    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("데이터를 저장하지 못했습니다.")



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

    def get_text(self, prompt):
        while True:
            text = input(prompt).strip()
            if text == "":
                print("내용을 입력해 주세요.")
                continue
            return text

    def add_quiz(self):
        print("새로운 퀴즈를 추가합니다.")
        question = self.get_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = self.get_text(f"선택지 {i}: ")
            choices.append(choice)
        answer = self.get_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("퀴즈가 추가되었습니다!")




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

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            self.save_state()
            print("새로운 최고 점수입니다!")



    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)


    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return
        print(f"최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct}문제 정답)")



    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.get_number("선택: ", 1, 5)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.save_state()
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("준비 중인 기능입니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 저장 후 종료합니다.")
            self.save_state()

