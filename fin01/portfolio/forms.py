from django import forms
from .models import Portfolio
class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name' , 'type' , 'description'  )
    def save(self, commit=True):
        portfolio = super(CreatePortfolioForm, self).save(commit=False)
        portfolio.user = self.user  # Thêm thông tin người dùng hiện tại
        if commit:
            portfolio.save()
        return portfolio