library(tidyverse)
library(magrittr)

is_not_empty <- function(string) {
  if(is.na(string) | string == "" | string == ".") {
    return(FALSE)
  } else {
    return(TRUE)
  }
}

is_not_empty = Vectorize(is_not_empty)

col_names <- c("Group ID", "ID", 
               "FF", "First Name", 
               "Last Name", "LF",
               "DoB", "Sex", "Race",
               "Reg No.", "First Name", "Last Name",
               "DoB", "Sex", "Race",
               "Record ID", "type","Same")

#[Group ID, Reg No., FF, First Name, Last Name, LF, 
# DoB, Race, Reg No., First Name, Last Name, 
#DoB, Race, Record ID, type, Answer]


(starred_data <- read_csv("./data_intermediate/all_starred_race.csv", 
                          col_types = cols(.default = "c", `Group ID` = "i")) %>%
  mutate_all(funs(ifelse(is_not_empty(.),.,""))) %>%
    mutate(src = str_extract(`Record ID`, "[AB]")) %>%
      rename(fname = `First Name`,
             lname = `Last Name`))



(starred_data <- 
  starred_data %>%
    mutate(`Record ID` = str_extract(`Record ID`,"[0-9]+")))

starred_data <- 
  starred_data %>%
  select(`Group ID`, `Reg No.`, FF, fname, lname, LF,
         DoB,Sex, Race, `Reg No._1`, `First Name_1`, `Last Name_1`, DoB_1,Sex_1, Race_1, 
         `Record ID`, type, Same) %>%
  arrange(as.numeric(`Group ID`))

# Reorganize confusing variable names
starred_data <- 
  starred_data %>% 
    rename(id = `Group ID`,
           type = `Record ID`,
           page = type)


set.seed(1)
# table for types corresponding to each group
df_type_group <- 
  tibble(
          type = c(1L, 7L, 13L, 19L, 25L, 31L, 4L, 8L, 14L, 26L, 3L, 10L, 15L,
                   27L, 2L, 11L, 17L, 9L, 16L, 28L, 6L, 23L, 18L, 29L, 24L, 36L,
                   20L, 32L, 5L, 21L, 33L, 12L, 22L, 34L, 30L, 35L) %>% as.character(),
         group = c(1L, 1L, 1L, 1L, 1L, 1L, 21L, 21L, 21L, 21L, 22L, 22L, 22L,
                   22L, 3L, 3L, 3L, 3L, 3L, 3L, 4L, 4L, 4L, 4L, 4L, 4L, 5L, 5L,
                   5L, 5L, 5L, 6L, 6L, 6L, 6L, 6L)
         ) 

# table for groups on each page
df_page_group <- 
  tibble(
    page = c(1L, 1L, 1L, 1L, 1L, 1L, 2L, 2L, 2L, 2L, 2L, 2L, 3L, 3L, 3L,
             3L, 3L, 3L, 4L, 4L, 4L, 4L, 4L, 4L, 5L, 5L, 5L, 5L, 5L, 5L,
             6L, 6L, 6L, 6L, 6L, 6L),
    group = c(1L, 21L, 22L, 3L, 4L, 5L, 1L, 2, 3L, 4L, 5L, 6L, 1L, 2, 3L,
              4L, 5L, 6L, 1L, 2, 3L, 4L, 5L, 6L, 1L, 2, 3L, 4L, 5L, 6L,
              1L, 21L, 22L, 3L, 4L, 6L)
  )

df_page_group <- df_page_group %>% as_tibble() %>% mutate_all(as.integer)

# if 2 pick, pick either 21 or 22 such that there are only 2 21s and 2 22s in the table
df_page_group[df_page_group$group == 2, "group"] <- sample(c(21,21,22,22),4)

# a table for each sample i, to keep removing the types we select in a page,
# so that they are not available for selection in the next page
# Basically ensures that all 36 types are selected. 
df_type_group_i <- df_type_group

# a table to store the selected types in each page  
df_target_page <- tibble()

for(page_i in 1:6){
  df_types_in_page_i <- 
    df_page_group %>% 
    filter(page == page_i) %>% 
    left_join(df_type_group_i, "group") %>% 
    group_by(page, group) %>% 
    sample_n(1) %>% 
    ungroup()
  
  df_target_page <- 
    df_target_page %>% 
    bind_rows(df_types_in_page_i)
  
  df_type_group_i <- 
    df_type_group_i %>% 
    anti_join(df_types_in_page_i, by = "type")
}

# create the lookup table by scrambling again (just to ensure the questions are scrambled even by group)
# the lookup has type and question_number 
lookup_scrambled <-
  df_target_page %>% 
  select(-group) %>% 
  group_by(page) %>% 
  sample_n(6) %>% 
  ungroup() %>% 
  mutate(qnum = row_number()) %T>%
  write_csv("scrambled_order.csv") %>% 
  select(-page)

attention_test <- 
  df_type_group %>% 
  filter(group == 1) %>% 
  pull(type)


for(i in 1:10) {
  

  # group by type and get one random pair for each type
  # sampling to ensure different samples get different questions
  ids_table <-
    starred_data %>%
    select(id, type) %>% 
    group_by(type) %>%
    sample_n(1) %>% 
    ungroup()
   
  # extract the data corresponding to the ids we filtered in step 1
  # this table is obviously not scrambled
  (sample_i <- 
      starred_data %>% filter(id %in% ids_table$id))
  
  # number and arrange by lookup
  sample_i_scrambled <- 
    sample_i %>%
    left_join(lookup_scrambled, by = "type") %>%
    arrange(qnum) %>% 
    select(-qnum) 
  
  #extract everything but those ids for section 2
  (section2  <- 
    starred_data %>%
    filter(!(id %in% ids_table$id)) %>%
    filter(!(type %in% attention_test)))
  
  (sec2_ids_scrambled <- 
    section2 %>%
    pull(id) %>%
    unique() %>% 
    sample(., length(.)))
  
  #we create a lookup for those gids
  (lookup_sec2 <- 
    tibble(id = sec2_ids_scrambled) %>%
    mutate(qnum = 1:n()))
  
  section2_scrambled <- 
    section2 %>%
    left_join(lookup_sec2, by = "id") %>%
    arrange(qnum) %>% 
    select(-qnum)

  # #make the names standard
  # names(sample_i) <- col_names
  # names(section2) <- col_names
  # names(sample_i_scrambled) <- col_names
  # names(section2_scrambled) <- col_names
  
  sample_i %>%
    write_csv(paste0("./data_output/samples_ordered/section1_",i,".csv"), col_names = F)
  section2 %>%
    write_csv(paste0("./data_output/samples_ordered/section2_",i,".csv"), col_names = F)
  
  sample_i_scrambled %>%
    write_csv(paste0("./data_output/samples_scrambled/section1_",i,".csv"), col_names = F)
  section2_scrambled %>%
    write_csv(paste0("./data_output/samples_scrambled/section2_",i,".csv"), col_names = F)
}

names(starred_data) <- col_names
write_csv(starred_data,"./data_output/main_section_full.csv", col_names = F)
# 
# starred_data %>%
#   sample_n(nrow(.)) %>%
#   write_csv("./data_output/section2.csv",col_names = F)
