from collections import defaultdict

'''Update date: May-01-2019'''
def compute_accuracy(gold_corpus, pred_corpus):
    assert len(gold_corpus) == len(pred_corpus) and len(gold_corpus) > 0
    correct = 0
    for gold, pred in zip(gold_corpus, pred_corpus):
        if gold == pred:
            correct += 1
    return correct / len(gold_corpus)

'''Reference url: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/bleu.py
Update date: April-30-2019'''
def compute_bleu(reference_corpus, generate_corpus, max_order=4, smooth=False):
    pass


'''Update date: April-30-2019'''
def _compute_f1(TP, FP, FN):
    precision = float(TP) / float(TP + FP) if TP + FP > 0 else 0
    recall = float(TP) / float(TP + FN) if TP + FN > 0 else 0
    f1 = 2. * ((precision * recall) / (precision + recall)) if precision + recall > 0 else 0
    return precision, recall, f1


'''Update date: April-30-2019'''
def compute_f1(gold_corpus, pred_corpus):
    assert len(gold_corpus) == len(pred_corpus)

    TP, FP, FN = defaultdict(int), defaultdict(int), defaultdict(int)
    for gold_sentence, pred_sentence in zip(gold_corpus, pred_corpus):
        gold_sentence = gold_sentence.strip().split("|") if len(gold_sentence.strip()) > 0 else []
        pred_sentence = pred_sentence.strip().split("|") if len(pred_sentence.strip()) > 0 else []

        for gold in gold_sentence:
            _, label = gold.split()
            if gold in pred_sentence:
                TP[label] += 1
            else:
                FN[label] += 1
        for pred in pred_sentence:
            _, label = pred.split()
            if pred not in gold_sentence:
                FP[label] += 1

    all_labels = set(TP.keys()) | set(FP.keys()) | set(FN.keys())
    metrics = {}
    for label in all_labels:
        precision, recall, f1 = _compute_f1(TP[label], FP[label], FN[label])
        metrics["precision-%s" % label] = precision
        metrics["recall-%s" % label] = recall
        metrics["f1-measure-%s" % label] = f1

    precision, recall, f1 = _compute_f1(sum(TP.values()), sum(FP.values()), sum(FN.values()))
    metrics["precision-overall"] = precision
    metrics["recall-overall"] = recall
    metrics["f1-measure-overall"] = f1

    return metrics


'''Update date: April-30-2019'''
def compute_discontinuous_f1(gold_corpus, pred_corpus):
    assert len(gold_corpus) == len(pred_corpus)

    gold_disc_corpus, pred_disc_corpus = [], []
    for gold_sentence, pred_sentence in zip(gold_corpus, pred_corpus):
        gold_mentions = gold_sentence.strip().split("|") if len(gold_sentence.strip()) > 0 else []
        discontinuous = [1 if len(m.split(" ")[0].split(",")) > 2 else 0 for m in gold_mentions]
        if sum(discontinuous) > 0:
            gold_disc_corpus.append(gold_sentence)
            pred_disc_corpus.append(pred_sentence)

    disc_metrics = compute_f1(gold_disc_corpus, pred_disc_corpus)

    metrics = compute_f1(gold_corpus, pred_corpus)
    for k, v in disc_metrics.items():
        metrics["discontinuous-%s" % k] = v

    return metrics
