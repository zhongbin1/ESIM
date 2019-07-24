# encoding: utf-8

import codecs
import numpy as np

def is_consist(cur, cur_next):
    if cur == 'o':
        return cur_next == 'o'
    elif cur == 'B-a':
        return cur_next == 'I-a'
    elif cur == 'I-a':
        return cur_next == 'I-a'
    elif cur == 'B-b':
        return cur_next == 'I-b'
    elif cur == 'I-b':
        return cur_next == 'I-b'
    elif cur == 'B-c':
        return cur_next == 'I-c'
    elif cur == 'I-c':
        return cur_next == 'I-c'

def get_result(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='utf-8_sig') as rfile:
        with codecs.open(output_file, 'w', encoding='utf-8_sig') as wfile:
            sent, tag = [], []
            for line in rfile.readlines():
                if line != '\n':
                    data = line.strip().split()
                    sent.append(data[0])
                    tag.append(data[2] if data[2] != 'O' else 'o')
                else:
                    if len(sent) > 0:
                        assert len(sent) == len(tag)
                        ret = ''
                        for index, s in enumerate(sent):
                            cur = tag[index]
                            if index + 1 < len(sent):
                                cur_next = tag[index + 1]
                                if is_consist(cur, cur_next):
                                    ret += s + '_'
                                else:
                                    if cur is 'o':
                                        ret += s + '/o' + '  '
                                    else:
                                        ret += s + '/' + cur[-1] + '  '

                            else:
                                if cur is 'o':
                                    ret += s + '/o' + '  '
                                else:
                                    ret += s + '/' + cur[-1]
                        wfile.write(ret.strip() + '\n')
                        sent.clear()
                        tag.clear()

def micro_f1(sub_lines, ans_lines, split = ' '):
    correct = []
    total_sub = 0
    total_ans = 0
    for sub_line, ans_line in zip(sub_lines, ans_lines):
        # print([sub_line], [ans_line])
        sub_line = set(str(sub_line).split(split))
        ans_line = set(str(ans_line).split(split))
        c = sum(1 for i in sub_line if i in ans_line) if sub_line != {''} else 0
        if c != len(sub_line) if sub_line != {''} else 0:
            print('pred_tag:', sub_line, 'true_tag:', ans_line)
        total_sub += len(sub_line) if sub_line != {''} else 0
        total_ans += len(ans_line) if ans_line != {''} else 0
        correct.append(c)
    p = np.sum(correct) / total_sub if total_sub != 0 else 0
    r = np.sum(correct) / total_ans if total_ans != 0 else 0
    f1 = 2*p*r / (p + r) if (p + r) != 0 else 0
    print('total sub:', total_sub)
    print('total ans:', total_ans)
    print('correct: ', np.sum(correct), correct)
    print('precision: ', p)
    print('recall: ',r)
    return 'f1',f1

def get_lines(sent, sub_tag, ans_tag):
    lines = []
    for tag in [sub_tag, ans_tag]:
        ret = ''
        for index, s in enumerate(sent):
            cur = tag[index]
            if index + 1 < len(sent):
                cur_next = tag[index + 1]
                if is_consist(cur, cur_next):
                    ret += s + '_'
                else:
                    if cur is 'o':
                        ret += s + '/o' + '  '
                    else:
                        ret += s + '/' + cur[-1] + '  '

            else:
                if cur is 'o':
                    ret += s + '/o' + '  '
                else:
                    ret += s + '/' + cur[-1]
        ret = ret.strip()
        temp = [lab for lab in ret.split('  ') if lab[-1] != 'o']
        if len(temp) == 0:
            r = ''
        else:
            r = ' '.join(temp)
        lines.append(r)

    return lines

def get_f1_score(input_file):
    sub_lines = []
    ans_lines = []
    with codecs.open(input_file, 'r', encoding='utf-8_sig') as rfile:
        sent, sub_tag, ans_tag = [], [], []
        for line in rfile.readlines():
            if line != '\n':
                data = line.strip().split()
                sent.append(data[0])
                sub_tag.append(data[2] if data[2] != 'O' else 'o')
                ans_tag.append(data[1] if data[1] != 'O' else 'o')
            else:
                if len(sent) > 0:
                    assert len(sent) == len(sub_tag) and len(sent) == len(ans_tag)
                    sub_line, ans_line = get_lines(sent, sub_tag, ans_tag)
                    sub_lines.append(sub_line)
                    ans_lines.append(ans_line)
                    sent.clear()
                    sub_tag.clear()
                    ans_tag.clear()
        f1_score = micro_f1(sub_lines, ans_lines)
        print(f1_score)



if __name__ == '__main__':
    # get_result('data/pred/test.preds.txt', 'data/pred/result.txt')
    pass








