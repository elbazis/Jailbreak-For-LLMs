from datetime import datetime


class JailbreakAttackRecord:
    def __init__(self, attack_name: str, attack_prompt: str, target_model: str,
                 model_response: str, timestamp: datetime, grade: float):
        """
        Initializes a JailbreakAttackRecord instance.

        :param attack_name: Name of the attack.
        :param attack_prompt: The jailbreak prompt.
        :param target_model: The target model of the attack.
        :param model_response: The target model's response to prompt
        :param timestamp: The time when the attack was created or recorded.
        :param grade: The grade of the attack, must be a float between 0 and 1 (inclusive).
        """
        self.attack_name = attack_name
        self.prompt = attack_prompt
        self.target_model = target_model
        self.model_response = model_response
        self.timestamp = timestamp
        self.grade = self._validate_grade(grade)

    @staticmethod
    def _validate_grade(grade: float) -> float:
        """Validates that the grade is a float between 0 and 1 (inclusive)."""
        if 0 <= grade <= 1:
            return grade
        raise ValueError("Grade must be a float between 0 and 1 (inclusive).")
