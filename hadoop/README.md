# Hadoop Python MapReduce Examples

Basis of this was from https://dev.to/boyu1997/run-python-mapreduce-on-local-docker-hadoop-cluster-1g46 but it didn't work because Python isn't available in the nodemanager.

# word_counter package

Counts the number of instances per each word.


```sh
echo "foo foo quux labs foo bar quux" | python -m hadoop.word_count.mapper |  sort -k1,1 | python -m hadoop.word_count.reducer
```

Produces an output:
```text
bar     1
foo     3
labs    1
quux    2
```


# social_media_connect package

Provices suggestions that based on mutual friends, possible friend connections; ie:

A   B
A   C
A   D

implies that user A is friends with B C and D.

This means that A is a mutal friend of each, and therefore they can be suggested to each other.

```sh
printf "A\tB\nA\tC\nA\tD\n" | python -m hadoop.social_media_connect.mapper | python -m hadoop.social_media_connect.reducer
```

or

```sh
printf "A\tB,C,D\nE\tB,C" | python -m hadoop.social_media_connect.mapper | python -m hadoop.social_media_connect.reducer
```

Produces an output:

```text
B       C,D
C       B,D
D       B,C
```


# Docker Test:

View on [NameNode](http://localhost:9870/)

[!WARNING]
(If you see an error Name node is in safe mode, re-run the map-reduce script.)


## Run MapReduce on [The Project Gutenberg eBook of Paradise Lost](https://www.gutenberg.org/cache/epub/20/pg20.txt)

```sh
scripts/build-hadoop.sh

scripts/test-map-reduce-word-count.sh
```

## Run MapReduce on [social_media_connections.txt](https://gist.githubusercontent.com/rcolfin/65515e06f7a9df787eb8684c0412a746/raw/911f098ce8fa55f4eaec0634805b0fb3d353f510/social_media_connections.txt)

The file is generated, but the test is to generate a list of potential connections for each person based on whether they have mutual friends.

```sh
scripts/build-hadoop.sh

scripts/test-map-reduce-social-media-connect
```

Expected output:

```text
B       C,D
C       B,D
D       B,C
```

## Building Docker Image

```sh
export BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
export GIT_COMMIT="$(git rev-parse --short HEAD)"
cd docker/nodemanager
docker compose build --pull
```
