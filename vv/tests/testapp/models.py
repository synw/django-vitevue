from django.db import models

SIDE = [("buy", "buy"), ("sell", "sell")]


class Agent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=255)
    agents = models.ManyToManyField(Agent, blank=True, related_name="markets")
    maker = models.ForeignKey(
        Agent, null=True, blank=True, on_delete=models.SET_NULL, related_name="market"
    )

    def __str__(self) -> str:
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Trade(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    side = models.CharField(max_length=4, choices=SIDE)

    def __str__(self) -> str:
        return f"${self.market} ${self.date}"
