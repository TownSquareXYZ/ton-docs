argparse 가져오기
가져오기 CSV
import re
가져오기 시스템

parser = argparse.ArgumentParser(description="TVM 명령어 참조 문서 생성")
parser.add_argument("instructions_csv", type=str, help="지침이 포함된 csv 파일")
parser.add_argument("doc_template", type=str, help="문서 템플릿")
parser.add_argument("out_file", type=str, help="출력 파일")
args = 파서.parse_args()

table_header = \
        "| xxxxxxx<br>Opcode " +\
        "| xxxxxxxxxxxxxxxx<br>다섯 번째 구문 " +\
        "| xxxxxxxxxxxxxxx<br>스택 " +\
        "| xxxxxxxxxxxxxxxxxxxx<br>설명 " +\
        "| xxxx<br>가스 |\n" +\
        "|:-|:-|:-|:-|:-|"

categories = dict()
cmd_to_name = dict()

열다(args.instructions_csv, "r")를 f로 사용합니다:
    reader = csv.DictReader(f)
    를 리더의 행에 입력합니다:
        cat = row["doc_category"]
        카테고리에 없는 경우
            categories[cat] = []
        categories[cat].append(row)
        if row["name"] != "":
            행["doc_fift"].split("\n"):
                s = s.strip()
                IF S != "":
                    s = s.split()[-1]
                    s가 cmd_to_name에 없는 경우:
                        cmd_to_name[s] = row["name"]

def name_to_id(s):
    반환 "instr-" + s.lower().replace("_", "-").replace("#", "SHARP")

def make_link(text, cmd):
    cmd_to_name에 cmd가 없는 경우:
        텍스트 반환
    name = cmd_to_name[cmd]
    반환 "[%s](#%s)" (text, name_to_id(name))

def gen_links(text):
    return re.sub("`([^ `][^`]* )?([A-Z0-9#-]+)`", lambda m: make_link(m.group(0), m.group(2)), text)

def make_table(cat):
    카테고리에 없는 경우
        print("그런 카테고리 없음", cat, file=sys.stderr)
        반환 ""
    table = [TABLE_HEADER]
    범주[cat]의 행에 대해
        opcode = row["doc_opcode"]
        fift = row["doc_fift"]
        스택 = row["doc_stack"]
        desc = row["doc_description"]
        gas = row["doc_gas"]

        IF OPCODE != "":
            opcode = "**`%s`**" % opcode

        IF FIFT != "":
            fift = "<br>".join("`%s`" % s.strip() for s in fift.split("\n")))

        IF 스택 != "":
            스택 = "_`%s`_" % 스택
            stack = stack.replace("|", "\\|")
            스택 = stack.strip()

        desc = desc.replace("|", "\\|")
        desc = desc.replace("\n", "<br>")

        if gas != "":
            gas = gas.replace("|", "\\|")
            gas = "`" + 가스 + "`"

        desc = gen_links(desc)
        desc = "<div id='%s'>" % name_to_id(row["name"]) + desc

        table.append("| %s | %s | %s | %s | %s |" % (opcode, five, stack, desc, gas))

    반환 "\n".join(table)

templ = open(args.doc_template, "r").read()

templ = gen_links(templ)

doc = re.sub("{{ *Table: *([a-zA-Z0-9_-]+) *}}", lambda m: make_table(m.group(1)), templ)
open(args.out_file, "w")를 f로 사용합니다:
    인쇄(문서, 파일=f)
