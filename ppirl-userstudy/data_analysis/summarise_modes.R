pacman::p_load(tidyverse, rebus)
key_info <- read_csv("parsed/df_u_key_info.csv")
View(key_info)


by_mode <- 
  key_info %>% 
  mutate(mode = str_sub(u_id,1,1))

by_mode[by_mode$u_id == 2004, "page_2_kapr"] = 2

by_mode %>% 
  group_by(mode) %>% 
  summarise_all(mean) %>% 
  select(mode, starts_with("page")) %>% 
  gather("page", "kapr", 2:7) %>% 
  mutate(page = str_extract(page, DGT) %>% as.integer()) %>% 
  ggplot(aes(page, kapr, col = mode)) +
  geom_line()
  
by_mode %>% 
  group_by(mode) %>% 
  summarise_all(mean) %>% 
  select(mode, starts_with("page")) %>% 
  select(mode, ends_with("score")) %>% 
  gather("page", "score", 2:7) %>% 
  mutate(page = str_extract(page, DGT) %>% as.integer()) %>% 
  ggplot(aes(page, score, col = mode)) +
  geom_line() 

by_mode %>% 
  group_by(mode) %>% 
  summarise_all(mean) %>% 
  select(mode, starts_with("page")) %>% 
  select(mode, ends_with("attention")) %>% 
  gather("page", "attention", 2:7) %>% 
  mutate(page = str_extract(page, DGT) %>% as.integer()) %>% 
  ggplot(aes(page, attention, col = mode)) +
  geom_line() 
  

gather("page2", "attention", 2:7) %>% 
  gather("page3", "score", 2:7) %>% 

by_mode %>% filter()


