from .models import LearningCharacteristic
from collections import defaultdict
import math

def naive_bayes_predict(selected_ids):
    categories = ['Visual', 'Auditory', 'Kinesthetic']
    prior_prob = 1 / len(categories)

    posterior = defaultdict(float)
    category_posterior = {}  # Untuk menyimpan perhitungan posterior per kategori

    for cat in categories:
        posterior[cat] = math.log(prior_prob)
        for sid in selected_ids:
            char = LearningCharacteristic.objects.get(id=int(sid))
            if char.category == cat:
                posterior[cat] += math.log(char.probability)
            else:
                posterior[cat] += math.log(1 - char.probability)

        category_posterior[cat] = posterior[cat]  # Menyimpan nilai posterior per kategori

    # Menentukan kategori dengan nilai posterior tertinggi
    predicted_category = max(posterior, key=posterior.get)

    return predicted_category, category_posterior
