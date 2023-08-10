import sys
from os.path import dirname
from sqlalchemy.orm import Session

sys.path.append(dirname(dirname(__file__)))
from src.resources.db_engine import slave_engine
import src.model as model


class SpeciesTrie:
    def __init__(self):
        self.species = self._get_species()
        self.trie = self._trie_init(self.species)

    def search(self, word: str) -> list:
        results = []
        if not word:
            return results

        trie = self.trie
        word = word.lower()

        for w in word:
            if w in trie:
                trie = trie[w]
            else:
                return results

        tasks = [trie]
        while tasks:
            task = tasks.pop()
            for key, value in task.items():
                if key == "end":
                    results.extend(value)
                else:
                    tasks.append(value)

        results = list(set(results))
        results.sort(reverse=True)
        return results

    def _trie_init(self, species) -> dict:
        trie = {}
        for sp in species:
            ans_name = (
                sp["chinese_common_name"]
                if sp["chinese_common_name"]
                else sp["english_common_name"]
            )
            taxon_name = sp["english_common_name"].split(" ")[-1].lower()
            ans = (sp["usage_count"], sp["taxon_order"], ans_name)
            if sp["chinese_common_name"]:
                trie = self._insert_trie(trie, sp["chinese_common_name"], ans)
            trie = self._insert_trie(trie, sp["english_common_name"].lower(), ans)
            trie = self._insert_trie(trie, taxon_name, ans)
            for code in sp["code"]:
                trie = self._insert_trie(trie, code.lower(), ans)
        return trie

    def _insert_trie(self, trie, word: str, ans):
        tmp_trie = trie
        for w in word:
            while w not in tmp_trie:
                tmp_trie[w] = {}
            tmp_trie = tmp_trie[w]
        if "end" in tmp_trie:
            tmp_trie["end"].append(ans)
        else:
            tmp_trie["end"] = [ans]
        return trie

    def _get_species(self) -> list[dict]:
        species = []
        taxon_order = 0

        with Session(slave_engine) as session:
            results = (
                session.query(
                    model.Species.taxon_order,
                    model.Species.chinese_common_name,
                    model.Species.english_common_name,
                    model.Species.usage_count,
                    model.SpeciesCodes.code,
                )
                .join(
                    model.SpeciesCodes,
                    model.SpeciesCodes.taxon_order == model.Species.taxon_order,
                    isouter=True,
                )
                .order_by(model.Species.taxon_order)
                .all()
            )

        for result in results:
            if taxon_order != result.taxon_order:
                d = result._asdict()
                d["code"] = []
                species.append(d)
                taxon_order = result.taxon_order
            if result.code:
                species[-1]["code"].append(result.code)
        return species


class SpeciesNames:
    def __init__(self) -> None:
        self._to_order_table = self._get_name_taxon_order_table()

    def get_taxon_orders(self, chinese_common_names: list[str]):
        return [
            self._to_order_table[name] if name in self._to_order_table else None
            for name in chinese_common_names
        ]

    def _get_name_taxon_order_table(self):
        with Session(slave_engine) as session:
            results = session.query(
                model.Species.chinese_common_name,
                model.Species.taxon_order,
            ).all()
        return {result.chinese_common_name: result.taxon_order for result in results}


if __name__ == "__main__":
    trie = SpeciesTrie()
    print(trie.search(""))
