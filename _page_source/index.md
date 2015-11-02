---
layout: post
title: pyg
description: "a graphing library in python"
category: code
tags: [python, visualization]
image:
  feature: "https://farm8.staticflickr.com/7014/6840341477_e49612bc59_o_d.jpg"
---

`pyg` (pronounce *pig*) is my graphing library for `python`, building off of
`matplotlib`.  Realistically, it only is very useful for a couple cases.

- If you're using my [`pym`](http://alexhagen.github.io/pym/) library for
interpolation, decimation, or other operations on data sets, `pyg` is a lazy
and easy way to create graphs from these objects.
- If you've got a specific style in mind, and you want to pass that in as an
`rc.Params` object, `pyg` can help you keep that style consistent.
- If you're wanting to publish, `pyg` has some exporting features that make
figures exported as *1-column*, *2-column*, or *full-page* look great in
journal articles.
- If you want to tinker, `pyg` is a good starting point for making functions
to consistently graph data with the same annotations, such as measurements,
data-pointers, and other features.
