import graphene
from graphene_django import DjangoObjectType

from .models import Link

# In GraphQL, a Type is an object that may contain multiple fields. 
# Each field is calculated through resolvers, that returns a value. 
# A collection of types is called a schema. 
# Every schema has a special type: Query and Mutation

# Query: retrieving data from server
class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

# Mutation: process of sending data to server

#1 Defines a mutation class. Right after, you define the output of the mutation, 
# the data the server can send back to the client. 
# The output is defined field by field for learning purposes.
# class CreateLink(graphene.Mutation):
#     id = graphene.Int()
#     url = graphene.String()
#     description = graphene.String()

#     #2 Defines the data you can send to the server
#     class Arguments:
#         url = graphene.String()
#         description = graphene.String()

#     #3 The mutation method: it creates a link in the database using the data sent by the user, 
#     # through the `url` and `description` parameters.
#     def mutate(self, info, url, description):
#         link = Link(url=url, description=description)
#         link.save()

#         # After, the server returns the CreateLink class with the data just created. 
#         # See how this matches the parameters set on #1
#         return CreateLink(
#             id=link.id,
#             url=link.url,
#             description=link.description,
#         )

#4 Creates a mutation class with a field to be resolved, 
# which points to our mutation defined before.
# class Mutation(graphene.ObjectType):
#     create_link = CreateLink.Field()

#5 Attaching Users to Links after authentication & authorization

from users.schema import UserType

# Change the CreateLink mutation to add posted_by (user)
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    # Add users (new)
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()
        
    def mutate(self, info, url, description):
        user = info.context.user or None
        
        # Add users (new)
        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        # Add users (new)
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )

# Redefined Mutation class
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()