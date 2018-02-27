import scrapy
import xml.etree.cElementTree as ET
import csv


class MainScraper(scrapy.Spider):
    name = "MainScraper"
    start_urls = [
        "https://www.disclosurequest.com/results?sortColumn=&sortDirection=&searchBox=&amountToBeRaisedMin=&amountToBeRaisedMax=&filingDateMin=&filingDateMax=&cikNumber=&page=1"]



    def __init__(self, name=None, **kwargs):
        super(MainScraper, self).__init__()

        # total_csv_name = "total.csv"
        # self.total_file = open(total_csv_name, 'w', encoding='utf-8', newline='')
        # self.writer = csv.writer(self.total_file)

        self.keys = [
            'sV', 'sT', 'tOL', 'pI_c', 'pI_eN', 'pI_iA_s1', 'pI_iA_s2', 'pI_iA_c', 'pI_iA_sOC', 'pI_iA_sOCD',
            'pI_iA_zC', 'pI_iPN', 'pI_jOI', 'pI_iPNL_v', 'pI_ePNL_v', 'pI_eT', 'pI_yOI_wFY', 'pI_yOI_v',
            'rPL_rPI_rPN_fN', 'rPL_rPI_rPN_lN', 'rPL_rPI_rPA_s1', 'rPL_rPI_rPA_s2', 'rPL_rPI_rPA_c', 'rPL_rPI_rPA_sOC',
            'rPL_rPI_rPA_sOCD', 'rPL_rPI_rPA_zC', 'rPL_rPI_rPRL_r', 'rPL_rPI_rC', 'rPL_rPI_rPN_fN_1',
            'rPL_rPI_rPN_lN_1', 'rPL_rPI_rPA_s1_1', 'rPL_rPI_rPA_s2_1', 'rPL_rPI_rPA_c_1', 'rPL_rPI_rPA_sOC_1',
            'rPL_rPI_rPA_sOCD_1', 'rPL_rPI_rPA_zC_1', 'rPL_rPI_rPRL_r_1', 'rPL_rPI_rC_1', 'rPL_rPI_rPN_fN_2',
            'rPL_rPI_rPN_lN_2', 'rPL_rPI_rPA_s1_2', 'rPL_rPI_rPA_s2_2', 'rPL_rPI_rPA_c_2', 'rPL_rPI_rPA_sOC_2',
            'rPL_rPI_rPA_sOCD_2', 'rPL_rPI_rPA_zC_2', 'rPL_rPI_rPRL_r_2', 'rPL_rPI_rC_2', 'rPL_rPI_rPN_fN_3',
            'rPL_rPI_rPN_lN_3', 'rPL_rPI_rPA_s1_3', 'rPL_rPI_rPA_s2_3', 'rPL_rPI_rPA_c_3', 'rPL_rPI_rPA_sOC_3',
            'rPL_rPI_rPA_sOCD_3', 'rPL_rPI_rPA_zC_3', 'rPL_rPI_rPRL_r_3', 'rPL_rPI_rC_3', 'oD_iG_iGT', 'oD_iG_iFI_iFT',
            'oD_iG_iFI_i40A', 'oD_iS_rR', 'oD_fEE_i', 'oD_fEE_i_1', 'oD_fEE_i_2', 'oD_tOF_nOA_iA', 'oD_tOF_dOFS_v',
            'oD_dOO_mTOY', 'oD_tOSO_iPIFT', 'oD_bCT_iBCT', 'oD_mIA', 'oD_sCL_r_rN', 'oD_sCL_r_rCRDN', 'oD_sCL_r_aBDN',
            'oD_sCL_r_aBDCRDN', 'oD_sCL_r_rA_s1', 'oD_sCL_r_rA_s2', 'oD_sCL_r_rA_c', 'oD_sCL_r_rA_sOC',
            'oD_sCL_r_rA_sOCD', 'oD_sCL_r_rA_zC', 'oD_sCL_r_sOSL_s', 'oD_sCL_r_sOSL_d', 'oD_sCL_r_sOSL_s_1',
            'oD_sCL_r_sOSL_d_1', 'oD_sCL_r_sOSL_s_2', 'oD_sCL_r_sOSL_d_2', 'oD_sCL_r_sOSL_s_3', 'oD_sCL_r_sOSL_d_3',
            'oD_sCL_r_sOSL_s_4', 'oD_sCL_r_sOSL_d_4', 'oD_sCL_r_sOSL_s_5', 'oD_sCL_r_sOSL_d_5', 'oD_sCL_r_sOSL_s_6',
            'oD_sCL_r_sOSL_d_6', 'oD_sCL_r_sOSL_s_7', 'oD_sCL_r_sOSL_d_7', 'oD_sCL_r_sOSL_s_8', 'oD_sCL_r_sOSL_d_8',
            'oD_sCL_r_sOSL_s_9', 'oD_sCL_r_sOSL_d_9', 'oD_sCL_r_sOSL_s_10', 'oD_sCL_r_sOSL_d_10', 'oD_sCL_r_sOSL_s_11',
            'oD_sCL_r_sOSL_d_11', 'oD_sCL_r_sOSL_s_12', 'oD_sCL_r_sOSL_d_12', 'oD_sCL_r_fS', 'oD_sCL_r_rN_1',
            'oD_sCL_r_rCRDN_1', 'oD_sCL_r_aBDN_1', 'oD_sCL_r_aBDCRDN_1', 'oD_sCL_r_rA_s1_1', 'oD_sCL_r_rA_s2_1',
            'oD_sCL_r_rA_c_1', 'oD_sCL_r_rA_sOC_1', 'oD_sCL_r_rA_sOCD_1', 'oD_sCL_r_rA_zC_1', 'oD_sCL_r_fS_1',
            'oD_oSA_tOA', 'oD_oSA_tAS', 'oD_oSA_tR', 'oD_i_hNAI', 'oD_i_tNAI', 'oD_sCFF_sC_dA', 'oD_sCFF_fF_dA',
            'oD_uOP_gPU_dA', 'oD_sB_aR', 'oD_sB_s_iN', 'oD_sB_s_sN', 'oD_sB_s_nOS', 'oD_sB_s_sT', 'oD_sB_s_sD'
        ]

        # self.writer.writerow(self.keys)

    def parse(self, response):
        urls = response.xpath("//tr[@class='detail']/td/div[4]/span[2]/a/@href").extract()
        company_names = response.xpath("//tr[@class='summary']/td[1]/text()").extract()

        for url, company_name in zip(urls, company_names):
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.getURL1, meta={"Company Name": company_name})

        # follow pagination link
        next_page_url = response.css("a.next-page.middle::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def getURL1(self, response):
        company_name = response.meta["Company Name"]
        # url = response.css('iframe#formFrame::attr(src)').extract_first()
        url = response.urljoin(
            response.xpath("//div[@class='sec-form-page']/label/select/option[2]/@value").extract_first())
        yield scrapy.Request(url=url, callback=self.getURL2, meta={"Company Name": company_name})

    def getURL2(self, response):
        company_name = response.meta["Company Name"]
        url = response.css('iframe#formFrame::attr(src)').extract_first()
        yield scrapy.Request(url=url, callback=self.parse_iframe, meta={"Company Name": company_name})

    def parse_iframe(self, response):
        company_name = response.meta["Company Name"]

        xmlTxt = response.text.split("<TEXT>")[1].split("</TEXT>")[0]
        xmlTxt = xmlTxt.replace('<?xml version="1.0"?>', "")
        root = ET.fromstring(xmlTxt)
        app = xmlParser(root, root.tag)
        result = app.result
        row = []

        for i, key in enumerate(self.keys):
            if key in result:
                row.append(result[key])
            else:
                row.append("")

        # self.writer.writerow(row)

        yield result
        # yield row

class xmlParser():
    def __init__(self, elem, elem_path=""):
        self.result = {}
        self.keys = []
        self.parse(elem, elem_path)

    def parse(self, elem, elem_path=""):
        for child in elem:
            if not child.getchildren() and child.text:
                path = "{}/{}".format(elem_path, child.tag)
                path = path.replace("XML/edgarSubmission/", "")
                path_sp = path.split("/")
                path_sp = [convertAbbr(elm) for elm in path_sp]
                path_abbr = "_".join(path_sp)
                value = child.text

                if self.keys.count(path_abbr) == 0:
                    # self.result.append([path, path_abbr, value])
                    self.result[path_abbr] = value
                else:
                    path_abbr_rev = path_abbr + "_{}".format(self.keys.count(path_abbr))
                    # self.result.append([path, path_abbr_rev, value])
                    self.result[path_abbr_rev] = value
                self.keys.append(path_abbr)
            else:
                self.parse(child, "{}/{}".format(elem_path, child.tag))


def convertAbbr(str):
    result = [str[0]] + [l for l in str if l.isupper() or l.isdigit()]
    return "".join(result)


if __name__ == '__main__':
    app = MainScraper()

"""
scrapy runspider main.py
scrapy runspider main.py -o items.json
more items.json

"""
