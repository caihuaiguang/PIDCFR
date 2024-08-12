# defualt set --average is True
# python scripts/parallel_run.py --algo CFR
# python scripts/parallel_run.py --algo CFRPlus
# python scripts/parallel_run.py --algo LinearCFR
# python scripts/parallel_run.py --algo DCFR
# python scripts/parallel_run.py --algo DCFRPlus --gamma=4 --alpha=1.5
# python scripts/parallel_run.py --algo PCFRPlus --gamma=2
# python scripts/parallel_run.py --algo PDCFRPlus --gamma=5 --alpha=2.3
# python scripts/parallel_run.py --algo PIDCFR


python scripts/parallel_run.py --algo CFR --average=False
python scripts/parallel_run.py --algo CFRPlus --average=False
python scripts/parallel_run.py --algo LinearCFR --average=False
python scripts/parallel_run.py --algo DCFR --average=False
python scripts/parallel_run.py --algo DCFRPlus --gamma=4 --alpha=1.5 --average=False
# python scripts/parallel_run.py --algo PCFRPlus --gamma=2 --average=False
# python scripts/parallel_run.py --algo PDCFRPlus --gamma=5 --alpha=2.3 --average=False
# python scripts/parallel_run.py --algo PIDCFR --average=False