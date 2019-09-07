import AnalysisEngine
import DrawingEngine

if __name__ == "__main__":
    url = 'http://fund.eastmoney.com/allfund.html#0'
    ae = AnalysisEngine.AnalysisEngine()
    # de = DrawingEngine.DrawingEngine()

    #ae.getContentByParsingUrl(url)
    #ae.extractFundsDetail()

    #ae.getFundLsjzByParsingUrl()
    ae.saveFundLsjzByCodeno('110011')
    # de.Draw('320004')

    print("Finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
