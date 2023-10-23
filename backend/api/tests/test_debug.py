


def insert_into_friends(redis_client):
    redis_client.sadd("friends:leto", "ghanima")
    redis_client.sadd("friends:leto", "duncan")
    redis_client.sadd("friends:paul", "duncan")
    redis_client.sadd("friends:paul", "gurney")


from pytest_mock_resources import create_redis_fixture

redis = create_redis_fixture()

def test_insert_into_friends(redis):
    insert_into_friends(redis)

    friends_leto = redis.smembers("friends:leto")
    friends_paul = redis.smembers("friends:paul")

    assert friends_leto == {b"duncan", b"ghanima"}
    assert friends_paul == {b"gurney", b"duncan"}
    