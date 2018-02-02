from unittest import TestCase
from os.path import dirname, join

from scorer import subtaskA, subtaskB

_ROOT_DIR = dirname(dirname(__file__))
_GOLD_FILE_A = join(_ROOT_DIR, 'data/gold/Task1-English-1st-Presidential.txt')
_PRED_FILE_A = join(_ROOT_DIR, 'data/scorer_tests/subtaskA_random_baseline.txt')
_GOLD_FILE_B = join(_ROOT_DIR, 'data/gold/Task2-English-1st-Presidential.txt')
_PRED_FILE_B = join(_ROOT_DIR, 'data/scorer_tests/subtaskB_random_baseline.txt')

class ScorerSubtaskA(TestCase):
    def test_average_precision(self):
        y_gold_labels = {1: 0, 2: 1, 3: 0, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]

        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=1)
        self.assertEqual(avg_p, 0)
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=2)
        self.assertEqual(avg_p, 0.5)
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=3)
        self.assertEqual(avg_p, 0.5)
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=5)
        self.assertEqual(avg_p, (0.5+0.4)/2)

        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=1)
        self.assertEqual(avg_p, 1)
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=3)
        self.assertEqual(avg_p, (1 + 2/3)/2)
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=5)
        self.assertEqual(avg_p, (1 + 2/3 + 3/5)/3)

        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 0}
        y_pred_ranked = [2, 4, 5, 1, 3]
        avg_p = subtaskA._compute_average_precision(y_gold_labels, y_pred_ranked, threshold=3)
        self.assertEqual(avg_p, 0)

    def test_precisions(self):
        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]
        prec = subtaskA._compute_precisions(y_gold_labels, y_pred_ranked, len(y_pred_ranked))
        self.assertEqual(prec, [1, 0.5, 2/3, 2/4, 3/5])

        y_gold_labels = {1: 0, 2: 0}
        y_pred_ranked = [1, 2]
        prec = subtaskA._compute_precisions(y_gold_labels, y_pred_ranked, len(y_pred_ranked))
        self.assertEqual(prec, [0, 0])

    def test_reciprocal_rank(self):
        y_gold_labels = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
        y_pred_ranked = [1, 2, 3, 4, 5]

        rr = subtaskA._compute_reciprocal_rank(y_gold_labels, y_pred_ranked, 1)
        self.assertEqual(rr, 1)
        rr = subtaskA._compute_reciprocal_rank(y_gold_labels, y_pred_ranked, 2)
        self.assertEqual(rr, 1)
        rr = subtaskA._compute_reciprocal_rank(y_gold_labels, y_pred_ranked, 3)
        self.assertEqual(rr, 1+1/3)
        rr = subtaskA._compute_reciprocal_rank(y_gold_labels, y_pred_ranked, 5)
        self.assertEqual(rr, 1+1/3+1/5)

    def test_read_gold_and_pred(self):
        gold_labels, pred_ranked = subtaskA._read_gold_and_pred(_GOLD_FILE_A, _PRED_FILE_A)

        self.assertEqual(list(gold_labels.keys()), [p[0] for p in pred_ranked])
        self.assertGreater(len([k for k, v in gold_labels.items() if v == 1]), 20)
        self.assertGreater(len([k for k, v in gold_labels.items() if v == 0]), 1000)


class ScorerSubtaskB(TestCase):
    def test_accuracy(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        self.assertEqual(subtaskB._compute_accuracy(conf_matrix), 3/18)

        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 0, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 0}}
        self.assertEqual(subtaskB._compute_accuracy(conf_matrix), 0/15)

    def test_recall(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        self.assertEqual(subtaskB._compute_macro_recall(conf_matrix), (0+2/7+1/6)/3)

        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 0, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 0}}
        self.assertEqual(subtaskB._compute_macro_recall(conf_matrix), (0 + 0 / 5 + 0 / 5) / 3)

    def test_f1(self):
        conf_matrix = {'true': {'true': 0, 'false': 2, 'half-true': 3},
                       'false': {'true': 2, 'false': 2, 'half-true': 3},
                       'half-true': {'true': 2, 'false': 3, 'half-true': 1}}
        p_true = 0
        r_true = 0
        p_false = 2/7
        r_false = 2/7
        p_half_true = 1/7
        r_half_true = 1/6
        self.assertEqual(subtaskB._compute_macro_f1(conf_matrix),
                         sum([2*p*r/(p+r) for p, r in zip([p_false, p_half_true],[r_false, r_half_true])])/3)

        conf_matrix = {'true': {'true': 0, 'false': 1, 'half-true': 0},
                       'false': {'true': 1, 'false': 0, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 1, 'half-true': 0}}

        self.assertEqual(subtaskB._compute_macro_f1(conf_matrix), 0)

    def test_read(self):
        gold_labels, pred_labels = subtaskB._read_gold_and_pred(_GOLD_FILE_B, _PRED_FILE_B)
        self.assertEqual(gold_labels.keys(), pred_labels.keys())
        self.assertGreater(len(gold_labels), 20)

    def test_conf_matrix(self):
        gold_labels = {1: 'true', 2: 'true', 3: 'half-true', 4: 'false'}
        pred_labels = {1: 'false', 2: 'true', 3:'false', 4: 'false'}

        conf_matrix = {'true': {'true': 1, 'false': 1, 'half-true': 0},
                       'false': {'true': 0, 'false': 1, 'half-true': 0},
                       'half-true': {'true': 0, 'false': 1, 'half-true': 0}}

        self.assertEqual(subtaskB._compute_confusion_matrix(gold_labels, pred_labels), conf_matrix)
