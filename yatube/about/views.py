from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Всем привет, меня зовут Коровин Игорь'
        context['job'] = '''В данный момент я работаю инженером'
                          по ремонту оргтехники'''
        context['future'] = '''Почему програмирование?
                            Потому что я выгорел на своей работе, хочется
                            кардинально поменять жизнь'''
        context['inspiration'] = '''Вдохновил меня мой товарищ,
                                 который смог (привет паровозик, ту-ту) в IT'''
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tools'] = '''При выполнении проекта был использован PyCharm,
                           с VSC как то не сложилось'''
        context['books'] = '''До практикума читал Лутца, поэтому
                           на начальном этапе было достаточно просто.
                           Но с продвижением далее по курсу становится
                           тяжелее. Django дается достаточно трудно.
                           Постоянно приходится перечитывать или
                           возвращаться на пару уроков назад,
                           чтоб усвоить всё.'''
        return context
