# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 13:16
# @Author  : shuai li
# description : ...

from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name='wechat_auto_ls',  # 包名称
    version='1.0',  # 版本
    author='shuai_li',  # 作者
    author_email='l1216710774@qq.com',  # 作者邮箱
    description='微信自动发送消息脚本',  # 描述
    long_description=readme(),  # 长文描述
    long_description_content_type='text/markdown',  # 长文描述的文本格式
    keywords='wechat',  # 关键词
    packages=find_packages(),
    url='https://github.com/HiNoName/wechat_auto',
    classifiers=[  # 包的分类信息，见https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.8',
    install_requires=['pywin32>=302', 'uiautomation>=2.0.18'],
    license='Apache License 2.0',  # 许可证
    scripts=['main/ls.py']
)


