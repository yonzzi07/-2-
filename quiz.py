class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question   # 문제
        self.choices = choices     # 선택지 4개 리스트
        self.answer = answer       # 정답 번호 (1~4)

    def display(self, number):
        print(f"[문제 {number}]")
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f" {i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


Quiz("1+1은?", ["1", "2", "3", "4"], 2).display(1)

