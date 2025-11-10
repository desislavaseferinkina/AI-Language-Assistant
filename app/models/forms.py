from pydantic import BaseModel, EmailStr

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

    def validate(self):
        errors = []
        if len(self.name.strip()) < 2:
            errors.append('Името е твърде кратко.')
        if len(self.message.strip()) < 5:
            errors.append('Съобщението е твърде кратко.')
        return errors