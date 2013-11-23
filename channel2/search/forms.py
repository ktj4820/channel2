from haystack.forms import SearchForm


class VideoSearchForm(SearchForm):

    def search(self):
        sqs = super().search()
        return sqs
