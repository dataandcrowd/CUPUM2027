# Checks of the LLM's reasoning (H-clock)

                                0       1       2        3        4        5
scenario                   NZ6_s1  NZ6_s2  NZ6_s3  NZ18_s1  NZ18_s2  NZ18_s3
llm_answers                   771     800     826      784      832      837
invalid                         0       0       0        0        0        0
fallbacks                       0       0       0        0        0        0
refusals                        0       0       0        0        0        0
charge_day_asked              617     610     639      547      549      574
llm_takes_gc_best_pct        58.8    58.7    59.6     60.3     58.5     60.8
rule_takes_gc_best_pct       87.1    88.8    87.1     94.4     93.8     92.8
same_response_as_rule_pct    57.7    56.1    57.0     59.8     59.4     60.1
llm_pt_where_rule_drives      121     123     127       97       94       89
rule_pt_where_llm_drives       38      46      45        9       13        8
rule_retimes                  151     135     134       84       90       97
llm_retimes                    42      38      37       26       28       28
money_quoted                  908     961     995     1255     1310     1303
money_traced_pct            100.0   100.0    99.9    100.0    100.0     99.8
clock_quoted                  244     290     306      321      359      368
clock_traced_pct            100.0   100.0   100.0    100.0    100.0    100.0
reviews                       120     122     139      205      215      216
reviews_kept_pct             98.3    96.7    99.3    100.0     99.5    100.0

## Charge-day answer (rows: LLM) against the rule's choice for the same commuter (columns)

scenario    LLM  PT  WFH  keep  retime
  NZ6_s1     PT  76    0    68      53
  NZ6_s1    WFH  11   10     5      12
  NZ6_s1   keep  33    3   244      60
  NZ6_s1 retime   5    2     9      26
  NZ6_s2     PT  80    3    85      38
  NZ6_s2    WFH   4   15     4       8
  NZ6_s2   keep  40    3   225      67
  NZ6_s2 retime   6    2     8      22
  NZ6_s3     PT  92    3    84      43
  NZ6_s3    WFH   7   15     8       3
  NZ6_s3   keep  38    2   238      69
  NZ6_s3 retime   7    5     6      19
 NZ18_s1     PT 253   67    49      48
 NZ18_s1    WFH   6   32     0       2
 NZ18_s1   keep   7    9    28      20
 NZ18_s1 retime   2   10     0      14
 NZ18_s2     PT 256   65    42      52
 NZ18_s2    WFH   2   36     1       1
 NZ18_s2   keep  11   14    19      22
 NZ18_s2 retime   2    9     2      15
 NZ18_s3     PT 264   64    45      44
 NZ18_s3    WFH   3   34     0       2
 NZ18_s3   keep   8   18    30      34
 NZ18_s3 retime   0    8     3      17

