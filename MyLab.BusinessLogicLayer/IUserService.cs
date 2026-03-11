namespace MyLab.BusinessLogicLayer;

public interface IUserService
{
    void RunMigration(string csvPath);
}