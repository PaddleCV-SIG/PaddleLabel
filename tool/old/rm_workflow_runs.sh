export TARGET_USER=PaddleCV-SIG
# export TARGET_REPO=PaddleLabel
export TARGET_REPO=PaddleLabel-ML
export TARGET_WORKFLOW_ID="xx.yml"

while :
do
    SIZE=$(gh api repos/$TARGET_USER/$TARGET_REPO/actions/workflows/$TARGET_WORKFLOW_ID/runs | jq -r .total_count)
    echo "Found: $SIZE"


    if [[ $SIZE -eq 0 ]]
    then
        echo "All done"
	break
    fi

    gh api repos/$TARGET_USER/$TARGET_REPO/actions/workflows/$TARGET_WORKFLOW_ID/runs | \
        jq -r '.workflow_runs[] | .id' | \
        xargs -n1 -I % gh api --silent repos/$TARGET_USER/$TARGET_REPO/actions/runs/% -X DELETE
    sleep 1
done
