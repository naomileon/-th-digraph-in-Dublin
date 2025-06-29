Create Strings as file list: "myList", "textgrids/*.TextGrid"
nbFiles = Get number of strings
writeFileLine: "results.txt", "speaker", tab$, "label"

for idx from 1 to nbFiles
        selectObject: "Strings myList"
        currentFile$ = Get string: idx

        underscore1 = index(currentFile$, "_")
        part1$ = mid$(currentFile$, 1, 2)
        part2$ = mid$(currentFile$, underscore1 + 1, 6)  ; <- Prend exactement 6 caractères après le 1er "_"
        currentSpk$ = part1$ + part2$

        Read from file: "textgrids/" + currentFile$
        nbInter = Get number of intervals: 2
        for jdx from 1 to nbInter
                currentLabel$ = Get label of interval: 2, jdx
                if currentLabel$ <> ""
                        appendFileLine: "results.txt", currentSpk$, tab$, currentLabel$
                endif
        endfor
endfor