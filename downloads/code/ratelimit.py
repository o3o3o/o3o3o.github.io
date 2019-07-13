from functools import wraps
from ratelimit.exceptions import Ratelimited
from ratelimit.utils import is_ratelimited


def GQLRatelimitKey(group, request):
    return request.gql_rl_field


def ratelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(root, info, **kw):
            request = info.context
            request.limited = getattr(request, "limited", False)

            new_key = key
            if key and key.startswith("gql:"):
                _key = key.split("gql:")[1]
                value = kw.get(_key, None)
                if not value:
                    raise ValueError(f"Cannot get key: {key}")
                request.gql_rl_field = value

                new_key = GQLRatelimitKey

            ratelimited = is_ratelimited(
                request=request,
                group=group,
                fn=fn,
                key=new_key,
                rate=rate,
                method=method,
                increment=True,
            )
            if ratelimited and block:
                raise Ratelimited
            return fn(root, info, **kw)

        return _wrapped

    return decorator

class Test(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)

    ok = graphene.Boolean()

    @ratelimit(key="ip", rate="10/m", block=True)
    @ratelimit(key="gql:phone", rate="5/m", block=True)
    def mutate(self, info, phone):
        request = info.context
        # Do sth
        return Test(ok=True)
