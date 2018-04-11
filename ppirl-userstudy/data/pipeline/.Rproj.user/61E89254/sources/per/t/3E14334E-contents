library(tidyverse)
library(magrittr)


# preprocessing -----------------------------------------------------------


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


# fixed sample distribution -----------------------------------------------

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


# distributions for 11 samples --------------------------------------------

attention_test <- 
  df_type_group %>% 
  filter(group == 1) %>% 
  pull(type)

ls_df_lookup_scrambled <- list()

df_type_n <- 
  starred_data %>% 
  group_by(id) %>% 
  slice(1) %>% 
  ungroup() %>% 
  count(type) %>% 
  arrange(n) %>% 
  mutate(n_remaining = n)


for(section in seq_len(11)){
  #initial selection
  df_lookup_scrambled_sec <-
    df_target_page %>% 
    select(-group) %>% 
    group_by(page) %>% 
    sample_n(6) %>% 
    ungroup() 
  
  (df_lookup_scrambled_sec <- 
      df_lookup_scrambled_sec %>% 
      left_join(df_type_n, by = "type") %>% 
      mutate(type = ifelse(n_remaining < 1, NA, type)) %>% 
      select(page, type))
  
  df_lookup_scrambled_sec_pos <- 
    df_lookup_scrambled_sec %>% 
    filter(!is.na(type)) %>% 
    mutate(type = map_chr(type, function(type_y){
      df_type_n$n_remaining[df_type_n$type == type_y] <<- df_type_n$n_remaining[df_type_n$type == type_y] - 1
      return(type_y)
    }))
  
  df_lookup_scrambled_sec_npos <- 
    df_lookup_scrambled_sec %>% 
    filter(is.na(type)) %>% 
    mutate(type = map2_chr(page, type, function(page_x, type_y){
      if(!is.na(type_y)){
        browser()
        df_type_n$n_remaining[df_type_n$type == type_y] <<- df_type_n$n_remaining[df_type_n$type == type_y] - 1
        return(type_y)
      } else{
        
        
        
        if(length(df_type_n$n_remaining[df_type_n$n_remaining < 0]) > 0){
          browser()
        }
        
        df_candidates_1 <- 
          df_type_n %>% 
          filter(n_remaining > 0)
        
        df_candidates_2 <- 
          df_candidates_1 %>% 
          filter(!type %in% attention_test)
        
        df_candidates_3 <- 
          df_candidates_2 %>% 
          filter(n == 12)
        
        df_candidates_4 <- 
          df_candidates_3 %>% 
          left_join(df_lookup_scrambled_sec, by = "type") %>% 
          filter(page != page_x) 
        
        replacement <- NA
        if(nrow(df_candidates_4) > 0){
          replacement <- df_candidates_4 %>% sample_n(1) %>% pull(type)
        } else if(nrow(df_candidates_3) > 0) {
          replacement <- df_candidates_3 %>% sample_n(1) %>% pull(type)
        } else if(nrow(df_candidates_2) > 0){
          replacement <- df_candidates_2 %>% sample_n(1) %>% pull(type)
        } else if(nrow(df_candidates_1) > 0){
          replacement <- df_candidates_1 %>% sample_n(1) %>% pull(type)
        }
        
        # message(replacement)
        # df_type_n %>% arrange(type) %>% print(n = 36)
        
        if(!is.na(replacement)){
          df_type_n$n_remaining[df_type_n$type == replacement] <<- df_type_n$n_remaining[df_type_n$type == replacement] - 1
        }
        
        # df_type_n %>% arrange(type) %>% print(n = 36)
        # message(section)
        
        
        return(replacement)
      }
    }))
  
  
  df_lookup_scrambled_sec <- 
    df_lookup_scrambled_sec_pos %>% 
    bind_rows(df_lookup_scrambled_sec_npos) %>% 
    filter(!is.na(type)) %>% print(n = 36)
  
  
  ls_df_lookup_scrambled[[section]] <- 
    df_lookup_scrambled_sec %>% 
    select(-page)%>% 
    mutate(qnum = row_number())
}

ls_df_lookup_scrambled %>% 
  bind_rows() %>% 
  count(type, sort = T)

df_id_sampling <- 
  starred_data %>% 
  select(id, type) %>% 
  group_by(id) %>% 
  slice(1) %>% 
  ungroup()

sample_df <- function(df){
  df %>% sample_n(df$n[1])
}

for(sample in seq_len(10)) {
  
  df_id_sampling_i <- df_id_sampling
  df_samples <- list()
  
  for(section in seq_len(11)) {
    # if(section == 6){
    #   browser()
    # }
    
    # browser()
    
    df_sampling_section <- 
      ls_df_lookup_scrambled[[section]] %>% 
      group_by(type) %>% 
      mutate(type_n = row_number()) %>% 
      ungroup()
      
    df_sampling_count <- df_sampling_section %>% count(type)

    df_sample_i_section_j <- 
      df_id_sampling_i %>% 
      left_join(df_sampling_count, "type") %>% 
      filter(!is.na(n)) %>% 
      group_by(type, n) %>% 
      nest() %>% 
      mutate(data = map2(data, n, ~sample_n(.x, .y))) %>% 
      unnest(data) %>% 
      group_by(type) %>% 
      mutate(type_n = row_number()) %>% 
      ungroup() %>% 
      left_join(df_sampling_section, by = c("type", "type_n")) %>% 
      arrange(qnum) %>% 
      select(-one_of("type", "n", "type_n"))
        
    # df_samplei_sectionj <- 
    #   df_id_sampling_i %>% 
    #   semi_join(sampling_section, "type") %>% 
    #   group_by(type) %>% 
    #   sample_n(1) %>% 
    #   ungroup() %>%
    #   left_join(sampling_section, "type") %>%
    #   ungroup() %>%
    #   select(-type)
    # 
    # if(section > 1) df_samplei_sectionj %>% semi_join(df_samples %>% bind_rows()) %>% print()
    # 
    df_id_sampling_i <-
      df_id_sampling_i %>%
      filter(!id %in% df_sample_i_section_j$id)
    # 
    # df_samples[[section]] <-    
    #   starred_data %>% 
    #   inner_join(df_samplei_sectionj, "id") %>% 
    #   arrange(qnum) %>% 
    #   select(-qnum)
    # 
    # df_samples %>% bind_rows() %>% count(type, id, sort = T) %>% mutate(n = n/2) %>% print()
    # 
    starred_data %>%
      inner_join(df_sample_i_section_j, "id") %>%
      arrange(qnum) %>%
      select(-qnum) %>%
      write_csv(str_c("data_output/samples_sections_scrambling/section_", section, "_sample_", sample, ".csv"), col_names = FALSE)
    
  }
  
}

