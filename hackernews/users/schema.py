from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

# Create users in mutation 

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


# Query user - listing all users
# class Query(graphene.ObjectType):
#     users = graphene.List(UserType)

#     def resolve_users(self, info):
#         return get_user_model().objects.all()

# Testing Authentication: add `me`
# PSst!! The GraphiQL web interface does not accept adding custom HTTP headers.
# To test this, use something like postman (desktop) and add token in headers
class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
