def preprocess():
    title_author_map = {}
    with open("parsed_title_author.txt") as f:
        for line in f:
            # Covert line to lowercase
            line = line.lower()
            cols = line.split("||")
            author = cols[0]
            #title = re.sub('[^a-z0-9 ]+', '', cols[1])
            title = cols[1]
            if title not in title_author_map:
                title_author_map[title] = []
                title_author_map[title].append(author)
            else:
                title_author_map[title].append(author)
    return title_author_map


def get_coauthor():
    coauthor_map = {}
    for title in title_author_map:
        for author in title_author_map[title]:
            if author not in coauthor_map:
                coauthor_map[author] = set()
                for other_author in title_author_map[title]:
                    if author != other_author:
                        coauthor_map[author].add(other_author)
            else:
                for other_author in title_author_map[title]:
                    if author != other_author:
                        coauthor_map[author].add(other_author)
    return coauthor_map


if __name__ == '__main__':
    title_author_map = preprocess()
    coauthor_map = get_coauthor()
    output = open("coauthor.txt", "w")
    for author, coauthors in coauthor_map.items():
        output.write(author + ": ")
        for coauthor in coauthors:
            output.write(coauthor+","+" ")
        output.write("\n")










