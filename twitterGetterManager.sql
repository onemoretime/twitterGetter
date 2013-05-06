SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `TwitterGetterDB` ;
CREATE SCHEMA IF NOT EXISTS `TwitterGetterDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `TwitterGetterDB` ;

-- -----------------------------------------------------
-- Table `TwitterGetterDB`.`TwitterUserName`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TwitterGetterDB`.`TwitterUserName` ;

CREATE  TABLE IF NOT EXISTS `TwitterGetterDB`.`TwitterUserName` (
  `idxTwitterUserName` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `screename` VARCHAR(45) NULL ,
  `image` BLOB NULL ,
  `imagefilename` VARCHAR(45) NULL ,
  `FullName` VARCHAR(45) NULL ,
  `Bio` VARCHAR(250) NULL ,
  `Location` VARCHAR(50) NULL ,
  `URL` VARCHAR(100) NULL ,
  PRIMARY KEY (`idxTwitterUserName`) ,
  UNIQUE INDEX `idxTwitterUserName_UNIQUE` (`idxTwitterUserName` ASC) ,
  UNIQUE INDEX `screename_UNIQUE` (`screename` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TwitterGetterDB`.`tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TwitterGetterDB`.`tweets` ;

CREATE  TABLE IF NOT EXISTS `TwitterGetterDB`.`tweets` (
  `idxTweets` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `idtweet` BIGINT NOT NULL ,
  `tweetContent` VARCHAR(500) NULL ,
  `tweetDate` DATETIME NULL ,
  PRIMARY KEY (`idxTweets`) ,
  UNIQUE INDEX `idxTweets_UNIQUE` (`idxTweets` ASC) ,
  UNIQUE INDEX `idtweet_UNIQUE` (`idtweet` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TwitterGetterDB`.`TwitterUserName_has_tweets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TwitterGetterDB`.`TwitterUserName_has_tweets` ;

CREATE  TABLE IF NOT EXISTS `TwitterGetterDB`.`TwitterUserName_has_tweets` (
  `TwitterUserName_idxTwitterUserName` INT UNSIGNED NOT NULL ,
  `tweets_idxTweets` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`TwitterUserName_idxTwitterUserName`, `tweets_idxTweets`) ,
  INDEX `fk_TwitterUserName_has_tweets_tweets1_idx` (`tweets_idxTweets` ASC) ,
  INDEX `fk_TwitterUserName_has_tweets_TwitterUserName_idx` (`TwitterUserName_idxTwitterUserName` ASC) ,
  CONSTRAINT `fk_TwitterUserName_has_tweets_TwitterUserName`
    FOREIGN KEY (`TwitterUserName_idxTwitterUserName` )
    REFERENCES `TwitterGetterDB`.`TwitterUserName` (`idxTwitterUserName` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TwitterUserName_has_tweets_tweets1`
    FOREIGN KEY (`tweets_idxTweets` )
    REFERENCES `TwitterGetterDB`.`tweets` (`idxTweets` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TwitterGetterDB`.`tinyURL`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TwitterGetterDB`.`tinyURL` ;

CREATE  TABLE IF NOT EXISTS `TwitterGetterDB`.`tinyURL` (
  `idxtinyURL` INT NOT NULL AUTO_INCREMENT ,
  `fqdnTinyURL` VARCHAR(45) NOT NULL COMMENT 'Table regroupant les fqdn des tinyURL connues' ,
  PRIMARY KEY (`idxtinyURL`) ,
  UNIQUE INDEX `fqdnTinyURL_UNIQUE` (`fqdnTinyURL` ASC) )
ENGINE = InnoDB;

USE `TwitterGetterDB` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
