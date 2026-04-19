from typing import cast

from rich import print as rprint

Tree = list[str | tuple[str, 'Tree']]


def rinput(prompt: object = ''):
    rprint(prompt, end='')
    return input()


def split_tree(tree: Tree, trait: str, split: set[str]) -> Tree:
    new_tree: Tree = [(trait, [])]

    for node in tree:
        if isinstance(node, tuple):
            new_tree.append((node[0], split_tree(node[1], trait, split)))
        elif node in split:
            cast(list, new_tree[0][1]).append(node)
        else:
            new_tree.append(node)

    if len(new_tree[0][1]) == 0:
        new_tree.pop(0)

    return new_tree


def sort_tree(tree: Tree, species: list[str], traits: list[str]) -> None:
    def by_input_order(node: str | tuple[str, Tree]):
        if isinstance(node, str):
            return species.index(node)
        else:
            sort_tree(node[1], species, traits)
            return traits.index(node[0])

    def species_first(node: str | tuple[str, Tree]):
        return 1 - isinstance(node, str)

    tree.sort(key=by_input_order)
    tree.sort(key=species_first)


def get_tree(species: dict[str, list[str]]) -> Tree:
    traits = list(set(sum(species.values(), [])))

    species_with_traits = {t: {s for s in species if t in species[s]} for t in traits}
    traits.sort(key=lambda t: len(species_with_traits[t]), reverse=True)

    tree: Tree = list(species.keys())

    for t in traits:
        tree = split_tree(tree, t, species_with_traits[t])

    sort_tree(tree, list(species.keys()), traits)

    return tree


def print_tree(tree: Tree, *, prefix: str = ''):
    """Inspired by https://stackoverflow.com/a/76691030"""
    for i, node in enumerate(tree):
        if isinstance(node, str):
            rprint(prefix, '└' if i == len(tree) - 1 else '├', '──', f'[bold blue]{node}[/bold blue]', sep='')
        else:
            rprint(prefix, '└' if i == len(tree) - 1 else '├', '──', f'[bold]{node[0]}[/bold]', sep='')
            print_tree(node[1], prefix=prefix + ('   ' if i == len(tree) - 1 else '│  '))


def main():
    n = int(rinput('[bold]Number of species:[/bold] '))

    species = dict()
    for _ in range(n):
        name = rinput('[bold]Name:[/bold] ')
        traits = rinput('[bold]Traits:[/bold] ').split()
        species[name] = traits

    tree = get_tree(species)

    print()
    rprint('[bold]Cladogram[/bold]')
    print_tree(tree)


if __name__ == '__main__':
    main()
