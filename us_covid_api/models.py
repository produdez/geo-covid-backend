from djongo import models
"""
    Dataset docs:
    v1: https://covidtracking.com/data/api (most description is here!)
    v2: https://covidtracking.com/data/api/version-2
"""

class State(models.Model):
    initials = models.CharField(max_length=2, unique=True)
    name = models.TextField(unique=True)
    class Meta:
        ordering = ['id']

class Polygon(models.Model):
    state_id = models.IntegerField(unique=True)
    state_name =  models.TextField(unique=True)
    state_initials = models.CharField(max_length=2, unique=True)
    type = models.TextField()
    coordinates = models.JSONField()

    class Meta:
        ordering = ['state_id']

    

class AbstractReport(models.Model):
    class Meta:
        abstract = True
    
    # ----------------------------------- Death ---------------------------------- #
    death = models.IntegerField(blank=True) # total deaths (confirmed + probable)
    death_confirmed = models.IntegerField(blank=True) # total confirmed deaths
    death_increase = models.IntegerField(blank=True) # new deaths today
    death_probable = models.IntegerField(blank=True) # total death with probable covid (non confirmed)

    # --------------------------------- Positive --------------------------------- #
    positive = models.IntegerField(blank=True) #  positive total (confirmed + probable people)
    positive_increase = models.IntegerField(blank=True) # new positive today (people)
    positive_cases_viral = models.IntegerField(blank=True) # confirmed positive (people)

    # --------------------------------- Negative --------------------------------- #
    negative = models.IntegerField(blank=True) # total negative (people)
    negative_increase = models.IntegerField(blank=True) # new negative today (people)
    # NOTE: seems to not have negative negative cases viral

    # ------------------------------- Hospitalized ------------------------------- #
    hospitalized_cumulative = models.IntegerField(blank=True) # cumulative hospitalized (ever)
    hospitalized_increase = models.IntegerField(blank=True) # new hospitalized today
    hospitalized_currently = models.IntegerField(blank=True) # currently hospitalized
    
    # ------------------------------------ ICU ----------------------------------- #
    in_icu_cumulative = models.IntegerField(blank=True) # cumulative in icu (ever)
    in_icu_currently = models.IntegerField(blank=True) # currently in icu
    
    # -------------------------------- Ventilator -------------------------------- #
    on_ventilator_cumulative = models.IntegerField(blank=True)
    on_ventilator_currently = models.IntegerField(blank=True)

    # ---------------------------------- Recover --------------------------------- #
    recovered = models.IntegerField(blank=True) # total recovered

    
    # -------------------------------- Total tests ------------------------------- #
    total_tests_people_viral = models.IntegerField(blank=True) # total unique people tested (people)
    total_tests_people_viral_increase = models.IntegerField(blank=True) # new unique people tested today (people)
    total_tests_viral = models.IntegerField(blank=True) # total tests (specimens)
    total_tests_viral_increase = models.IntegerField(blank=True) # new tests (specimens)

    # NOTE: positive_tests_viral + negative_tests_viral != total_tests_viral
    #   (But the sum is a near approximation, means it could be due to failed test)
    positive_tests_viral = models.IntegerField(blank=True) # total positive (specimens)
    negative_tests_viral = models.IntegerField(blank=True) # total negative (specimen)

    # ---------------------------------- Erroneous --------------------------------- #
    hospitalized = models.IntegerField(blank=True) # ! deprecated (but basically same as hospitalized_cumulative)
    positive_score = models.IntegerField(blank=True) # ! deprecated
    # ! dangerous, quote: "At the national level, this metric is a summary statistic which, because of the variation in test reporting methods, is at best an estimate of US viral (PCR) testing."
    total_test_results = models.IntegerField(blank=True) 
    # ! dangerous, quote: "we recommend against using it at the state/territory level."
    total_test_results_increase = models.IntegerField(blank=True)

# ---------------------------------- USELESS --------------------------------- #
    # ------------------------------- Antibody Test ------------------------------ #
    total_tests_antibody = models.IntegerField(blank=True) # total antibody test (specimens)
    total_tests_people_antibody = models.IntegerField(blank=True) # total unique people antibody test (people)
    positive_tests_antibody = models.IntegerField(blank=True) # total positive antibody test (specimens)
    positive_tests_people_antibody = models.IntegerField(blank=True) # total unique people w/ positive antibody test (people)
    negative_tests_antibody = models.IntegerField(blank=True)
    negative_tests_people_antibody = models.IntegerField(blank=True)
    
    # ------------------------------- Antigen Tests ------------------------------ #
    total_tests_antigen = models.IntegerField(blank=True) # total antigen test (specimens)
    total_tests_people_antigen = models.IntegerField(blank=True) # total unique people antigen test (people)
    positive_tests_antigen = models.IntegerField(blank=True) # total positive antigen test (specimens)
    positive_tests_people_antigen = models.IntegerField(blank=True)  # total unique people w/ positive antigen test (people)
    # NOTE: seems to not have negative tests antigen in data and api doc
    
    # ---------------------------------- Others ---------------------------------- #
    # These two attribute have no meaning for story telling
    total_test_encounters_viral = models.IntegerField(blank=True) # total tests done (1 person counts as 1 each day)
    total_test_encounters_viral_increase = models.IntegerField(blank=True) # total people tested today

class Report(AbstractReport):
    class Meta:
        unique_together = (('date','state'))
        indexes = [
            models.Index(fields=['date']),
        ]
        ordering = ['date']

    date = models.DateTimeField()
    state = models.ForeignKey(State, on_delete=models.CASCADE) # NOTE: state have index by default being a ForeignKey (https://stackoverflow.com/questions/5984842/does-django-automatically-generate-indexes-for-foreign-keys-columns)

class GlobalReport(AbstractReport):
    class Meta:
        indexes = [
            models.Index(fields=['date']),
        ]
        ordering = ['date']

    date = models.DateTimeField(unique=True)
    states = models.IntegerField()

