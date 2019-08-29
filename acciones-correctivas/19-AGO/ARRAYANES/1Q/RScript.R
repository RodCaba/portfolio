# ACCIONES CORRECTIVAS ARRAYANES #
#######LIBRARIES########
libraries <- c('tidyverse', 'lubridate', 'readxl')
lapply(libraries, require, character.only = TRUE)

######LOAD DATA #####
met <- read_excel('dat/Engine Status Report_20190827_123509.xlsx', sheet = 'Report',
                  skip = 4)

#####TIDY DATA#######
met <- met %>% 
  separate(Vehículo, into = 'Unidad', sep = '\\s', extra = 'drop') %>% 
  separate(Valor, into = 'valor', sep = '\\s', extra = 'drop') 
  
met <- met %>% 
  select(Unidad, Fecha, Descripción, valor) %>% 
  mutate(valor = as.numeric(valor))

km <- met %>% 
  group_by(Unidad,Descripción) %>% 
  filter(Descripción == 'Odómetro') %>% 
  summarize(km = ((max(valor) - min(valor))/1000))

l <- met %>% 
  group_by(Unidad, Descripción) %>% 
  filter(Descripción == 'Cantidad total de combustible utilizado') %>% 
  summarize(litros =  max(valor) - min(valor))

######JOIN DATA AND SUMMARIZE###########
met <- full_join(km, l, by = 'Unidad')

met <- met %>%
  select(Unidad, km, litros) %>% 
  mutate(rend_met = km / litros)

met <- met %>% 
  mutate(rend_obj = case_when(
    Unidad == 'S-30' ~ 3.80,
    Unidad == 'S-33' ~ 3.80,
    TRUE ~ 3.60))

met <- met %>% 
  mutate(litros_obj = km/rend_obj)

met <- met %>% 
  mutate('(+)AHORRO/(-)PÉRDIDA LITROS' = litros_obj - litros)

ah_per_quincenal <- sum(met$`(+)AHORRO/(-)PÉRDIDA LITROS`)

write_excel_csv(met,'output/rend.csv')
