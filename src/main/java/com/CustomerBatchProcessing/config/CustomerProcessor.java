package com.CustomerBatchProcessing.config;

import com.CustomerBatchProcessing.model.Customer;
import org.springframework.batch.item.ItemProcessor;

public class CustomerProcessor implements ItemProcessor<Customer, Customer> {

    @Override
    public Customer process(Customer item) throws Exception {
        return item;
    }
}
