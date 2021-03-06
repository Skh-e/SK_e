from django.shortcuts import render

# from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .recipes import RECIPES, INGREDIENTS, images_map

IMAGES = images_map(INGREDIENTS)


class IntroPage(Page):
    def vars_for_template(self):
        return dict(
            BasePay=Constants.BasePay
        )


class IntroPage2(Page):
    def vars_for_template(self):
        return dict(
            employeepercent=100 * Constants.EmployeeRatio,
            managerpercent=100 * Constants.ManagerRatio
        )


class CultureCondition(Page):
    pass


class Randomization(Page):
    timeout_seconds = 15


class PlayerIntroPage(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2, 3)

    def vars_for_template(self):
        return dict(
            employeepercent=100 * Constants.EmployeeRatio,
            managerpercent=100 * Constants.ManagerRatio
        )


class GameIntro(Page):
    pass


class ComprehensionSurvey(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class SPComprehensionSurvey(Page):
    def is_displayed(self):
        return self.player.id_in_group == 3

class SPBefWait(Page):
    pass

class WRound1(WaitPage):
    pass

class WRound2(WaitPage):
    pass

class WRAlloc(WaitPage):
    pass

class LocationChoice(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.id_in_group == 1:
            return ['NLocationChoice']
        else:
            return ['SLocationChoice']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class LocationApproval(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class SandwichIntro(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class Shop(Page):
    live_method = "handle_message"

    def vars_for_template(self):
        return dict(ingredients=INGREDIENTS, menu=RECIPES)

    def js_vars(self):
        return dict(duration=180, menu=RECIPES, images=IMAGES)

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class AfterPractice(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

    # Reset Game Values
    def before_next_page(self):
        self.player.reset_after_practice()


class Round1(Page):
    live_method = "handle_message"

    def vars_for_template(self):
        return dict(ingredients=INGREDIENTS, menu=RECIPES)

    def js_vars(self):
        return dict(duration=300, menu=RECIPES, images=IMAGES)

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class AfterRound1Game(Page):
    timeout_seconds = 15

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class AfterRound2Game(Page):
    timeout_seconds = 15
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class AnnounceSalesRound1(Page):
    def vars_for_template(self):
        ownshare = self.player.revenue * 0.5
        supervisorshare = self.player.revenue * 0.25
        firmshare = self.player.revenue * 0.25
        return dict(ownshare=ownshare,supervisorshare=supervisorshare,firmshare=firmshare)
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class RiskEvent(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

class ReportingScreen(Page):
    form_model = 'player'
    def vars_for_template(self):
        ownshare = self.player.revenue * 0.5
        supervisorshare = self.player.revenue * 0.25
        firmshare = self.player.revenue * 0.25
        return dict(ownshare=ownshare,supervisorshare=supervisorshare,firmshare=firmshare)
    def get_form_fields(self):
        if self.player.id_in_group == 1:
            if self.group.reportingcondition == 'mandatory':
                return ['NReportedPerf', 'NReportedRiskManD']
            else:
                return ['NReportedPerf', 'NReportedRiskVol']
        else:
            if self.group.reportingcondition == 'mandatory':
                return ['SReportedPerf', 'SReportedRiskManD']
            else:
                return ['SReportedPerf', 'SReportedRiskVol']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class ReminderAccess(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class AfterRound1Report(Page):
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class SPLocation1(Page):
    def is_displayed(self):
        return self.player.id_in_group == 3

class WLocation(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 3

class SPLocation2(Page):
    form_model = 'player'

    def vars_for_template(self):
        return dict(
            northernlocation=self.group.get_player_by_id(1).NLocationChoice,
            southernlocation=self.group.get_player_by_id(2).SLocationChoice
        )

    def is_displayed(self):
        return self.player.id_in_group == 3


class SPBefReporting(Page):
    def is_displayed(self):
        return self.player.id_in_group == 3


class SPAllocation(Page):
    form_model = 'player'
    form_fields = ['Stime', 'Ntime', 'SEM', 'NEM']

    def vars_for_template(self):
        return dict(
            northernreportedperformance=self.group.get_player_by_id(1).NReportedPerf,
            northernmandatoryrisk=self.group.get_player_by_id(1).NReportedRiskManD,
            northernvoluntaryrisk=self.group.get_player_by_id(1).NReportedRiskVol,
            southernreportedperformance=self.group.get_player_by_id(2).SReportedPerf,
            southernmandatoryrisk=self.group.get_player_by_id(2).SReportedRiskManD,
            southernvoluntaryrisk=self.group.get_player_by_id(2).SReportedRiskVol
        )

    def error_message(self, values):
        print('Allocated', values)
        if values['Stime'] + values['Ntime'] > 10:
            return 'You can allocate a maximum of 10 minutes to the two regional managers.'
        if values['Stime'] + values['Ntime'] < 10:
            return 'Please allocate the full 10 minutes to the two regional managers.'

    def is_displayed(self):
        return self.player.id_in_group == 3

class SPAfterAllocation(Page):
    def is_displayed(self):
        return self.player.id_in_group == 3


class expectancy1(Page):
    form_model = 'player'
    form_fields = ['extime']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class expectancy2(Page):
    form_model = 'player'
    form_fields = ['exbudget', 'exshort', 'exlong']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

class expectancy3(Page):
    form_model = 'player'
    form_fields = ['expect1', 'expect2', 'expect3']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)
class riskperception1(Page):
    form_model = 'player'
    form_fields = ['riskiden']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class riskperception2(Page):
    form_model = 'player'
    form_fields = ['riskperc', 'riskcert', 'riskseri']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

    def before_next_page(self):
        self.player.set_up_second_round()
        self.player.handleriskevent()


class riskimpexexp(Page):
    form_model = 'player'
    form_fields = ['riskimp1', 'riskimp2']
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

class Sriskimpexexp(Page):
    form_model = 'player'
    form_fields = ['riskimp1', 'riskimp2']
    def is_displayed(self):
        return self.player.id_in_group == 3


class AfterRound1Allocation(Page):
    def vars_for_template(self):
        return dict(
    emergencynorth = self.group.get_player_by_id(3).NEM,
    emergencysouth = self.group.get_player_by_id(3).SEM)
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class Round2(Page):
    live_method = "handle_message"

    def vars_for_template(self):
        return dict(ingredients=INGREDIENTS, menu=RECIPES)

    def js_vars(self):
        return dict(duration=60 * self.player.time, menu=RECIPES, images=IMAGES)

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)
    def before_next_page(self):
        self.player.calcrevenue()


class AnnounceSalesRound2(Page):
    def vars_for_template(self):
        if self.player.riskmaterialized == 1:
            ownshare = self.player.revenue * 0.5 * 0.7
            supervisorshare = self.player.revenue * 0.25 * 0.7
            firmshare = self.player.revenue * 0.25 * 0.7
        else:
            ownshare = self.player.revenue * 0.5
            supervisorshare = self.player.revenue * 0.25
            firmshare = self.player.revenue * 0.25
        return dict(ownshare=ownshare,supervisorshare=supervisorshare,firmshare=firmshare)
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class PostExpQuest(Page):
    def vars_for_template(self):
        ownshare = (self.player.revenue + self.player.revenueR1) * 0.5
        return dict(ownshare=ownshare)
    def is_displayed(self):
        return self.player.id_in_group in (1, 2)

class riskimportpostexp(Page):
    form_model = 'player'
    form_fields = ['riskimp3', 'riskimp4', 'riskimp5']

class factor1(Page):
    form_model = 'player'
    form_fields = ['factor1', 'factor2', 'factor3', 'factor4', 'factor5', 'factor6', 'factor7', "factor8"]

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class factor2(Page):
    form_model = 'player'
    form_fields = ['factor9', 'factor10', 'factor11', 'factor12', 'factor13', 'factor14', 'factor15']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class supimpress1(Page):
    form_model = 'player'
    form_fields = ['sup1', 'sup2', 'sup3', 'sup4', 'sup5']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class supimpress2(Page):
    form_model = 'player'
    form_fields = ['sup6', 'sup7', 'sup8', 'sup9', 'sup10']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class orgtrust(Page):
    form_model = 'player'
    form_fields = ['trust1', 'trust2', 'trust3', 'trust4', 'trust5', 'trust6']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class suptrust(Page):
    form_model = 'player'
    form_fields = ['suptrust1', 'suptrust2', 'suptrust3', 'suptrust4', 'suptrust5', 'suptrust6']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class manvoluntarycheck(Page):
    form_model = 'player'
    form_fields = ['manvol1', 'manvol2', 'manvol3']


class responsibility(Page):
    form_model = 'player'
    form_fields = ['resp1', 'resp2']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class reportquality(Page):
    form_model = 'player'
    form_fields = ['repq1', 'repq2']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class uncertaversion1(Page):
    form_model = 'player'
    form_fields = ['unc1', 'unc2', 'unc3', 'unc4', 'unc5', 'unc6']


class uncertaversion2(Page):
    form_model = 'player'
    form_fields = ['unc7', 'unc8', 'unc9', 'unc10', 'unc11', 'unc12']


class volexp(Page):
    form_model = 'player'
    form_fields = ['mandatory', 'voluntary']

    def get_form_fields(self):
        if self.group.reportingcondition == 'mandatory':
            return ['mandatory']
        else:
            return ['voluntary']


class perf(Page):
    form_model = 'player'
    form_fields = ['perf1', 'perf2']

    def is_displayed(self):
        return self.player.id_in_group in (1, 2)


class riskattitude1(Page):
    form_model = 'player'
    form_fields = ['riskat1', 'riskat2', 'riskat3', 'riskat4', 'riskat5', 'riskat6']


class riskattitude2(Page):
    form_model = 'player'
    form_fields = ['riskat7', 'riskat8', 'riskat9', 'riskat10', 'riskat11']


class optimism(Page):
    form_model = 'player'
    form_fields = ['opt1', 'opt2', 'opt3', 'opt4', 'opt5', 'opt6']


class dark(Page):
    form_model = 'player'
    form_fields = ['dark1', 'dark2', 'dark3', 'dark4', 'dark5', 'dark6', 'dark7', 'dark8', 'dark9', 'dark10', 'dark11',
                   'dark12']


class pclosure1(Page):
    form_model = 'player'
    form_fields = ['closure1', 'closure2', 'closure3', 'closure4', 'closure5', 'closure6', 'closure7']

    def is_displayed(self):
        return self.player.id_in_group == 3


class pclosure2(Page):
    form_model = 'player'
    form_fields = ['closure8', 'closure9', 'closure10', 'closure11', 'closure12', 'closure13', 'closure14', 'closure15']

    def is_displayed(self):
        return self.player.id_in_group == 3


class uncertainaversion1(Page):
    form_model = 'player'
    form_fields = ['unc1', 'unc2', 'unc3', 'unc4', 'unc5', 'unc6']


class uncertainaversion2(Page):
    form_model = 'player'
    form_fields = ['unc7', 'unc8', 'unc9', 'unc10', 'unc11', 'unc12']


class allocationfactor1(Page):
    form_model = 'player'
    form_fields = ['sfact1', 'sfact2', 'sfact3', 'sfact4', 'sfact5']

    def is_displayed(self):
        return self.player.id_in_group == 3


class allocationfactor2(Page):
    form_model = 'player'
    form_fields = ['sfact7', 'sfact8', 'sfact9', 'sfact10', 'sfact6','sfact11']

    def is_displayed(self):
        return self.player.id_in_group == 3


class emergencyfactor(Page):
    form_model = 'player'
    form_fields = ['emfact1', 'emfact2', 'emfact3', 'emfact4', 'emfact5', 'emfact6']

    def is_displayed(self):
        return self.player.id_in_group == 3


class reportqual1(Page):
    form_model = 'player'
    form_fields = ['north1', 'north2', 'south1', 'south2']

    def is_displayed(self):
        return self.player.id_in_group == 3

class mansafetycheck(Page):
    form_model = 'player'
    form_fields = ['safety1', 'safety2', 'safety3', 'safety4', 'safety5', 'safety6', 'safety7']

class GenQuest(Page):
    form_model = 'player'
    form_fields = ['gen1', 'gen2', 'gen3', 'gen4']


class Results(Page):
    def vars_for_template(self):
        ownshare = self.player.ownshare
        supervisorshare = self.group.get_player_by_id(1).supervisorshare + self.group.get_player_by_id(2).supervisorshare
        total = self.player.revenue + self.player.revenueR1
        return dict(ownshare=ownshare, supervisorshare=supervisorshare)


page_sequence = [IntroPage, IntroPage2, CultureCondition, Randomization, PlayerIntroPage, GameIntro,
                 LocationChoice, SPLocation1,WLocation, LocationApproval, SPLocation2, SandwichIntro, Shop, AfterPractice,
                 ComprehensionSurvey, SPComprehensionSurvey, SPBefWait, WRound1, SPBefReporting, Round1, AfterRound1Game, AnnounceSalesRound1,
                 RiskEvent, ReportingScreen, WRAlloc, AfterRound1Report, SPAllocation,
                 SPAfterAllocation, expectancy1, expectancy2, expectancy3, riskperception1, riskperception2,
                 riskimpexexp,
                 AfterRound1Allocation, WRound2, Sriskimpexexp,Round2, AfterRound2Game, AnnounceSalesRound2, PostExpQuest,
                 allocationfactor1, allocationfactor2, responsibility,
                 riskimportpostexp, reportqual1, supimpress1, supimpress2,
                 reportquality, orgtrust, suptrust, reportimp, perf,
                 emergencyfactor, factor1, factor2, riskattitude1, riskattitude2, pclosure1, pclosure2,
                 uncertainaversion1, uncertainaversion2, optimism, dark, mansafetycheck, manvoluntarycheck, volexp,
                 GenQuest, Results]
