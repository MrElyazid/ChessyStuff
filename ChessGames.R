library(bigchess)
library(dplyr)
library(ggplot2)
library(tidyr)
library(e1071)
library(stringr)


# Games importation
games <- read.pgn("D:/mygames.pgn")


# Converting the date column to Date object 
games$Date = as.Date(games$Date, format = "%Y.%m.%d")


# ********* Charts and Visual stuff *********

# *** Piechart for Frequency of games for each day of the week ***


games$DayOfWeek <- weekdays(games$Date)
day_counts <- table(games$DayOfWeek)
day_percentages <- round(day_counts / sum(day_counts) * 100, 1)
labels <- paste(names(day_counts), day_percentages, "%")
colors <- rainbow(length(day_counts))

pie(day_counts,
    labels = labels,
    main = "Days of the Week Played",
    col = colors,    
    border = "white",
    cex = 0.8        
)

legend("topright",
       legend = names(day_counts),
       fill = colors,
       title = "Day of Week"
)


# *** Number of Moves played in games, histogram ***

mean_moves <- mean(games$NMoves)
skewness_moves <- skewness(games$NMoves)
kurtosis_moves <- kurtosis(games$NMoves)

hist(games$NMoves, 
     breaks = 50, 
     col = "skyblue", 
     main = "Number of Moves Per Game", 
     xlab = "Number of Moves", 
     ylab = "Frequency", 
     border = "white")

lines(density(games$NMoves), col = "red", lwd = 2)
abline(v = mean_moves, col = "darkgreen", lwd = 2, lty = 2)

legend("topright", 
       legend = c(paste("Mean: ", round(mean_moves, 2)),
                  paste("Skewness: ", round(skewness_moves, 2)),
                  paste("Kurtosis: ", round(kurtosis_moves, 2))),
       col = c("darkgreen", "black", "black"),
       lwd = c(2, NA, NA),
       lty = c(2, NA, NA),
       bty = "n",
       text.col = "black")


# *** Bar chart for the Frequency of win/loss/draw ***

outcome_counts <- c(Wins = sum((games$Result == "1-0" & games$White == "Mr_Elyazid") |
                                 (games$Result == "0-1" & games$Black == "Mr_Elyazid")),
                    Draws = sum(games$Result == "1/2-1/2"),
                    Losses = sum((games$Result == "0-1" & games$White == "Mr_Elyazid") | 
                                   (games$Result == "1-0" & games$Black == "Mr_Elyazid")))

outcome_percentages <- round((outcome_counts / sum(outcome_counts)) * 100, 2)
bar_colors <- c("green", "yellow", "red")

barplot_heights <- barplot(outcome_counts, 
                           main = "Game Outcomes", 
                           xlab = "Result", 
                           ylab = "Frequency", 
                           col = bar_colors, 
                           border = "white", 
                           ylim = c(0, max(outcome_counts) * 1.2), 
                           names.arg = c("Wins", "Draws", "Losses"),
                           cex.names = 0.8)


text(x = barplot_heights, 
     y = outcome_counts, 
     labels = paste(outcome_percentages, "% with ", outcome_counts, " games"), 
     pos = 3, 
     cex = 0.8, 
     col = "black")


legend("top",
       legend = c("Wins", "Draws", "Losses"), 
       fill = bar_colors, 
       title = "Outcomes",
       bty = "n")




# ********* Special Games  *********
# *** The Game with the most Captures ***


most_captures_game = games[which.max(sapply(games$Movetext,
                                            function(moves) str_count(moves, "x"))), ]
print(most_captures_game$Site)


# *** Longest Game ***
longest_game = games[which.max(games$NMoves), ]
print(longest_game$Site)


# *** Game with the most king moves ***
longest_Kmoves = games[which.max(games$K_moves), ]
print(longest_Kmoves$Site)

# *** Game with the most Rook moves ***
longest_Rmoves = games[which.max(games$R_moves), ]
print(longest_Rmoves$Site)

# *** Game with the most Queen moves ***
longest_Qmoves = games[which.max(games$Q_moves), ]
print(longest_Qmoves$Site)


# *** Game with the most Bishop moves ***
longest_Bmoves = games[which.max(games$B_moves), ]
print(longest_Bmoves$Site)


# *** Game with the most Knight moves ***
longest_Nmoves = games[which.max(games$N_moves), ]
print(longest_Nmoves$Site)

# *** King move resulting in mate ***
checkmateKing_games <- games[grepl("K", games$last.move) & grepl("#", games$last.move), ]




# ******* Most Frequent Opponents *******

most_frequent_opponents <- sort(table(c(games$White, games$Black)), decreasing = TRUE)

# exclude myself from the most frequent opponents
top_opponents <- most_frequent_opponents[2:10]
bar_colors <- rainbow(length(top_opponents))

barplot(top_opponents, 
        main = "Most Frequent Opponents", 
        ylab = "Frequency", 
        las = 2, 
        col = bar_colors, 
        border = "white", 
        ylim = c(0, max(top_opponents) * 1.2))

text(x = seq_along(top_opponents), 
     y = top_opponents, 
     labels = top_opponents, 
     pos = 3, 
     cex = 0.8, 
     col = "black")

legend("topright", 
       legend = names(top_opponents), 
       fill = bar_colors, 
       title = "Opponents", 
       cex = 0.6)
