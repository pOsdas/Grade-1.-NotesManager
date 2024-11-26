class Note:
    def __init__(
            self,
            title,
            content,
            status,
            created_date,
            issue_date,
    ):
        self.title: str = title
        self.content: str = content
        self.status: str = status
        self.created_date: str = created_date
        self.issue_date: str = issue_date

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "created_date": self.created_date,
            "issue_date": self.issue_date,
        }

    @staticmethod
    def from_dict(
            self,
            title,
            content,
            status,
            created_date,
            issue_date,
    ):
        return Note(title=title, content=content, status=status, created_date=created_date, issue_date=issue_date)

    def __str__(self):
        return f"Заметка: Заголовок: {self.title}, Содердание: {self.content}, Статус: {self.status}, Дата создания: {self.created_date}, Дата истечения: {self.issue_date}"
