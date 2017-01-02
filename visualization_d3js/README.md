## Data Visualization: Titanic Dataset Exploration

### Summary
The datset contains the demographics and passenger information from 891 of the 2224 passengers and crew on board the Titanic. survival : Survival (0 = No; 1 = Yes) class : Passenger Class (1 = 1st; 2 = 2nd; 3 = 3rd).
The first visualization shows the survival rates as per the gender and number of siblings of each person present on the titanic. The second visualization shows the survival rates w.r.t gender and class.

### Design
I chose the Titanic dataset: giving passenger information aboard RMS Titanic. On April 15, 1912, the Titanic sank after colliding with an iceberg. One of the reasons that the shipwreck was the unavailibility of lifeboats for the passengers and crew. Some groups of people were more likely to survive than others, such as women, children, and the upper-class. The visualization for the explored dataset is plotted. 
The dataset is explored for such patterns and the visualizations are plotted on demonstrate the findings. 

I chose to work with dimple.js as it would be sufficient and effective for this task:

Since I have comparative data that I would like to represent through a chart then a bar chart would be the best option. This type of chart is one of the more familiar options as it is easy to interpret. These charts are useful for displaying data that is classified into nominal or odinal categories.


Patterns explored:

-> Survival rate variation as per number of siblings
-> Survival rate variation as per class
-> Survival rate variation as per sex


Findings from the explorations: 

1. The survival rate of female passengers was much greater than that of male passengers. From a total of 577 male passengers, only 109 i.e less than 20 percent survived. However, out of the total 314 female passengers, 233 i.e upto 74 percent of the female population aboard survived. 

2. There is a heirarchy in the titanic w.r.t class of the passenger. The passenger who were rich i.e. are from the 1st class had the greater rate of survival irrespective oh the gender. 62.96 percent of the 1st class passengers survived whereas, the survival percentage amongst the third class passengers was only a third of this.

3. It is observed that the rate of survival is higher for the passengers travelling with family as compared to those travelling alone.
The survival rate of female passengers was much greater than that of male passengers. 

### Before feedback:
The html made before feedback can be found in: original.html

### Feedback

#### #1

> The overall visualization is good. But you can show proportion of people survived instead of the count of the people.Also increase the height of the bars to make it more informative. This would be a better way of representing data. This also makes charts easily understable to readers.

#### #2

> It is given in easy to understand format. Your chart was a bit less informative as survival ratio just shows upto one decimal place. It should be atleast upto two decimal places. Also try to order your x part properly arranged in numerical sequence order. 

####  #3

> The charts are intuitive even though not named properly. With proper headings it would look better. The charts are boring and can use some more colors and text to give it a better feel. Also you can draw one or more charts other than bar graph like scatter plots and line plots. 

 

### After Feedback:
Certain changes are made:
- One more plot is drawn between Age and survival Rate 
- Proportion of people survived is added
- I showed survival proportions upto 2 decimal places using tickFormat function
- Findings from the chart 
- Result of the data exploration
- Red bubbles are used for the scatter plot


The html made after feedback can be found in: finaln.html

### Results
 -> The female passengers with less number of siblings had greater chances of survival.
 ->Higher class passengers had greater chances of survival.
 ->Most of the passengers of age b/w 15-30 were survived.
 

### Resources


- (https://www.udacity.com/course/viewer#!/c-ud507-nd)
- (https://www.kaggle.com/c/titanic)
- (http://dimplejs.org/)
