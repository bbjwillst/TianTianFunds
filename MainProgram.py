import AnalysisEngine
import DrawingEngine

if __name__ == "__main__":
    url = 'http://fund.eastmoney.com/allfund.html#0'
    ae = AnalysisEngine.AnalysisEngine()
    # de = DrawingEngine.DrawingEngine()

    #ae.getContentByParsingUrl(url)
    #ae.extractFundsDetail()

    #ae.getFundLsjzByParsingUrl()
    # 110003 易方达上证50指数A       110011 易方达中小盘         161725 招商中正白酒指数分级           161726 招商国证生物医药指数分级
    # 260108 景顺长城新兴成长混合     320004 诺安优化收益债券     501047 汇添富中证全指证券公司指数A     519697 交银优势行业混合
    ae.saveFundLsjzByCodenoList(['110003', '110011', '161725', '161726', '260108', '320004', '501047', '519697'])
    # de.Draw('320004')

    print("Finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
