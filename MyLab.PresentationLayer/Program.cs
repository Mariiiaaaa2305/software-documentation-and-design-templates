using MyLab.BusinessLogicLayer;
using MyLab.DataAccessLayer;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

IUserRepository repo = new UserRepository();
IUserService service = new UserService(repo);

string filePath = "data_users.csv";

while (true)
{
    Console.WriteLine("\nAvailable commands:");
    Console.WriteLine("create - generate CSV file");
    Console.WriteLine("load   - import users into database");
    Console.WriteLine("close  - exit program");

    Console.Write("Enter command: ");

    string command = Console.ReadLine()?.ToLower() ?? "";

    switch (command)
    {
        case "create":

            using (StreamWriter writer = new StreamWriter(filePath))
            {
                writer.WriteLine("Id,Name,Email");

                for (int i = 1; i <= 1000; i++)
                {
                    writer.WriteLine($"{i},User_{i},user{i}@mail.com");
                }
            }

            Console.WriteLine("CSV file successfully created.");
            break;

        case "load":

            Console.WriteLine("Starting data import...");

            service.RunMigration(filePath);

            Console.WriteLine("Data import finished.");
            break;

        case "close":

            Console.WriteLine("Application closed.");
            return;

        default:

            Console.WriteLine("Unknown command.");
            break;
    }
}