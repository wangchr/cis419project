import matplotlib.pyplot as plt

plt.switch_backend('TKAgg')

x_frac = [0.01, 0.04, 0.06, 0.1, 0.2, 0.4, 0.6, 0.8]
x = [frac * 6233 for frac in x_frac]

unweighted = [0.581025873808, 0.662453183521, 0.671049486015, 0.704619225968,
              0.743539325843, 0.765168539326, 0.76404494382, 0.778651685393]
weighted = [0.621425329097, 0.660112359551, 0.673918240497, 0.716853932584,
            0.746629213483, 0.771161048689, 0.78595505618, 0.793258426966]

plt.plot(x, weighted, label="Weighted")
plt.plot(x, unweighted, label="Unweighted", linestyle='--')
plt.xlabel('Number of Training Recipes')
plt.ylabel('Accuracy (%)')
plt.legend(loc=4)
plt.title('Classifier Accuracy')
plt.show()
