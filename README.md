# Weekly-Papers-in-arXiv
The name of this project is to get weekly papers in arXiv. Run the `weekly_dp.py`, then a markdown file in the past week with keyworkds 'differential privacy' or 'differentially private'.

# Requirements
- Python3.8
- arxiv (pip install arxiv)

# More Usage

There are three arguments in this project, which are:
- keywords: to filter what papers you want
- filename: the output filename
- link: arxiv link, the default arxiv link is set as: [https://arxiv.org/list/cs.CR/pastweek?show=120](https://arxiv.org/list/cs.CR/pastweek?show=120)

```shell
python weekly_dp.py
python weekly_dp.py --keywords 'differential privacy, differentially private'
python weekly_dp.py --filename 'output.md'
```

If you want to find papers with keywords 'Reinforcement Learning' in cs.AI, you can use the link argument. For example
```shell
python weekly_dp.py --keywords 'reinforcement learning' --link 'https://arxiv.org/list/cs.AI/pastweek?show=120'
```



