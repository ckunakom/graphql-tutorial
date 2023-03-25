import graphene
import graphql_jwt
import links.schema

############################ links ############################
# Step 1 Query
# class Query(links.schema.Query, graphene.ObjectType):
#     pass

# schema = graphene.Schema(query=Query)

# Step 2 Mutation
# class Mutation(links.schema.Mutation, graphene.ObjectType):
#     pass

# schema = graphene.Schema(query=Query, mutation=Mutation)

############################# users ############################
# Step 3 Add user to mutation
import users.schema

# class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType,):
#     pass


# Step 4 Add the users.schema.Query (Add users to query)
# -- Enable the users query in the main query class:
class Query(users.schema.Query, links.schema.Query, graphene.ObjectType):
    pass

# schema = graphene.Schema(query=Query, mutation=Mutation)

# Step 5 Configuring django-graphql-jwt for authentication
class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# Same as above - looks like schema has to be defined after class is defined
schema = graphene.Schema(query=Query, mutation=Mutation)