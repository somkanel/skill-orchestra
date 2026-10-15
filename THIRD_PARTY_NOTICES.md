# Third-party notices / 第三方说明

本项目角色编排与命名说明的组织方式参考 [Video Circus](https://github.com/somkanel/video-circus)。评分与包装程序为本项目编写，不包含该项目的视频处理代码。

Python 是外部运行依赖，不随本项目分发。GitHub Actions 使用 actions/checkout 和 actions/setup-python，由 GitHub 在工作流执行时提供，不包含在技能运行时。技能结构校验使用本机 skill-creator 的校验器及临时环境 PyYAML，均不作为运行依赖打包。

Role-based orchestration and the naming introduction were inspired by Video Circus. No video processing code, third-party source, binaries or models are bundled. Python is a separate runtime. CI actions and optional external skill validators are development tools, not skill runtime dependencies.
