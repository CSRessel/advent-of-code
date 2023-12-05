alias n := new
alias d := download
alias s := solve
alias w := watch

new problem year="2023" lang="py":
    #!/usr/bin/env bash
    set -euxo pipefail
    echo "New {{lang}} solution for {{year}}/{{problem}}"
    if [[ "{{lang}}" =~ "^(py|js)$" ]]; then echo "ERROR: unsupported language {{lang}}"; exit 1; fi
    PROBLEM_DIR="{{year}}/{{problem}}"
    if [[ -n "$(ls -A $PROBLEM_DIR)" ]]; then echo "{{year}}/{{problem}} not empty"; exit 1; fi
    mkdir -p $PROBLEM_DIR
    cp scaffolding/template.{{lang}}  "$PROBLEM_DIR/day{{problem}}.{{lang}}"

download problem year="2023":
    #!/usr/bin/env bash
    set -euxo pipefail
    INPUT="{{year}}/{{problem}}/input"
    touch $INPUT
    echo "not implemented"

solve problem year="2023" lang="py":
    #!/usr/bin/env bash
    set -euxo pipefail
    TARGET="{{year}}/{{problem}}/day{{problem}}.{{lang}}"
    INPUT="{{year}}/{{problem}}/input"
    if [[ ! -f $TARGET ]]; then echo "couldn't find target ${TARGET}"; exit 1; fi
    if [[ ! -f $INPUT ]]; then echo "no input yet in ${INPUT}"; exit 1; fi
    if [[ {{lang}} == "py" ]]; then python3 $TARGET;
    else
        echo "couldn't recognize language type for $TARGET"; exit 1;
    fi

submit problem year="2023" part="1":
    #!/usr/bin/env bash
    set -euxo pipefail
    echo "not implemented"

watch problem year="2023":
    find "{{year}}/{{problem}}" | entr -s "just s {{problem}}"
