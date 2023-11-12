from textual.validation import Validator, ValidationResult

class HasOneSpace(Validator):
    def validate(self, value: str) -> ValidationResult:
        print('VALIDATION:', self, value)
        return (
            self.success()
            if (c := value.count(' ')) == 1
            else self.failure('Too many spaces' if c else 'No spaces')
        )

