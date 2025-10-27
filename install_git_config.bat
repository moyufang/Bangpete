@echo off
echo Installing Git aliases...

REM 新功能提交
git config alias.feat "!f() { git add . && git commit -m \"feature(*@$1): $2\"; }; f"
git config alias.featb "!f() { git add . && git commit -m \"feature(b@$1): $2\"; }; f"
git config alias.featf "!f() { git add . && git commit -m \"feature(f@$1): $2\"; }; f"

REM Bug修复提交  
git config alias.fix "!f() { git add . && git commit -m \"fix(*@$1): $2\"; }; f"
git config alias.fixb "!f() { git add . && git commit -m \"fix(b@$1): $2\"; }; f"
git config alias.fixf "!f() { git add . && git commit -m \"fix(f@$1): $2\"; }; f"

REM 代码微调：代码风格调整、过程算法优化
git config alias.tune "!f() { git add . && git commit -m \"tune(*@$1): $2\"; }; f"
git config alias.tuneb "!f() { git add . && git commit -m \"tune(b@$1): $2\"; }; f"
git config alias.tunef "!f() { git add . && git commit -m \"tune(f@$1): $2\"; }; f"

REM 测试相关
git config alias.test "!f() { git add . && git commit -m \"test(*@$1): $2\"; }; f"
git config alias.testb "!f() { git add . && git commit -m \"test(b@$1): $2\"; }; f"
git config alias.testf "!f() { git add . && git commit -m \"test(f@$1): $2\"; }; f"

REM 重构提交：涉及项目结构大刀阔斧的整改
git config alias.refa "!f() { git add . && git commit -m \"refactor: $1\"; }; f"

REM 文档
git config alias.doc "!f() { git add . && git commit -m \"doc: $1\"; }; f"

REM 杂项：如更新依赖、资源等等
git config alias.chore "!f() { git add . && git commit -m \"chore: $1\"; }; f"

REM 自定义类型
git config alias.cmit "!f() { git add . && git commit -m \"$1(*@$2): $3\"; }; f"
git config alias.cmitb "!f() { git add . && git commit -m \"$1(b@$2): $3\"; }; f"
git config alias.cmitf "!f() { git add . && git commit -m \"$1(f@$2): $3\"; }; f"

echo Git aliases installed successfully!
echo.
echo Usage examples:
echo   git featb "module" "description"
echo   git fixf "component" "fix something"