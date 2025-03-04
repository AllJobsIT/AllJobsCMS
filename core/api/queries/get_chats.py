import graphene
from graphene_django import DjangoObjectType

from core.models import ChatIds


class ChatNode(DjangoObjectType):
    all_chat = graphene.List(graphene.String)

    class Meta:
        model = ChatIds
        only_fields = ['all_chat', 'message']

    def resolve_all_chat(self: ChatIds, info):
        all_chat = []
        for chat_block in self.chats:
            all_chat.append(chat_block.value['chat_id'])
        return all_chat


class ChatQuery:
    get_chat = graphene.Field(ChatNode)

    def resolve_get_chat(self, info, **kwargs):
        chat = ChatIds.objects.all().first()
        return chat