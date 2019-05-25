# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SearchCondition:
    base = ""
    category = []
    includes = []
    excludes = []
    folder = ""
    alias = ""
    description = ""

    def __init__(self, base, category, includes, excludes, folder, alias, description):
        self.base = base
        self.category = category
        self.includes = includes
        self.excludes = excludes
        self.folder = folder
        self.alias = alias
        self.description = description

    def toString(self):
        return self.base + " : " + self.alias

searchConditions = [
    SearchCondition("蟠龙1元新", ["清代邮票", "民国邮票"], ["蟠龙1元"], ["石印"], "coiling_dragon_1d_mint", "1dm", "大清蟠龙邮票 壹圆新票"),
    SearchCondition("蟠龙1元旧", ["清代邮票", "民国邮票"], ["蟠龙1元"], ["石印"], "coiling_dragon_1d_used", "1du", "大清蟠龙邮票 壹圆旧票"),
    SearchCondition("蟠龙2元新", ["清代邮票", "民国邮票"], ["蟠龙2元"], ["石印"], "coiling_dragon_2d_mint", "2dm", "大清蟠龙邮票 贰圆新票"),
    SearchCondition("蟠龙2元旧", ["清代邮票", "民国邮票"], ["蟠龙2元"], ["石印"], "coiling_dragon_2d_used", "2du", "大清蟠龙邮票 贰圆旧票"),
    SearchCondition("蟠龙5元新", ["清代邮票", "民国邮票"], ["蟠龙5元"], ["石印"], "coiling_dragon_5d_mint", "5dm", "大清蟠龙邮票 伍圆新票"),
    SearchCondition("蟠龙5元旧", ["清代邮票", "民国邮票"], ["蟠龙5元"], ["石印"], "coiling_dragon_5d_used", "5du", "大清蟠龙邮票 伍圆旧票"),
    ]
